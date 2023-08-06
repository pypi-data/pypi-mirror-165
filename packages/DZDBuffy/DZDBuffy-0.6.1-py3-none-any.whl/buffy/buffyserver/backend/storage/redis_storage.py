import datetime
from urllib import response
import uuid
import logging
from io import FileIO
from typing import Dict, List, overload, Literal, AsyncGenerator, Union
import redis
from pathlib import Path, PurePath
import hashlib

import asyncio
from buffy.buffyserver.api.v1.models import (
    Response,
    Request,
    Request_in,
    ResponsePinClaim,
    ResponseTagClaim,
)
from buffy.tools.utils import url_to_path_dir_name
from buffy.buffyserver.backend.storage.interface import StorageInterface

log = logging.getLogger(__name__)


class RedisStorage(StorageInterface):
    HASHING_ALG = hashlib.md5
    KEY_BASE: str = "bfy"
    KEY_REQUESTS: str = f"{KEY_BASE}:reqs"
    KEY_RESPONSES: str = f"{KEY_BASE}:resp"
    KEY_TAG_CLAIMS: str = f"{KEY_BASE}:tag"
    KEY_PIN_CLAIMS: str = f"{KEY_BASE}:pin"

    def __init__(
        self,
        file_storage_dir: Path = Path("./buffycache"),
        config={"host": "localhost", "port": 6379},
    ):
        self.db = redis.Redis(**config)
        self.files_base = (
            file_storage_dir
            if isinstance(file_storage_dir, Path)
            else Path(file_storage_dir)
        )
        self.open_file_ios: Dict[Response, FileIO] = {}

    def test_connection(self) -> bool:
        try:
            res = self.db.info()
            if res:
                return True
            else:
                return False
        except redis.exceptions.ConnectionError as e:
            log.error(e)
            log.error("Redis Connection not possible")
            return False

    def _generate_id(self) -> str:
        # as we will work with fairly low quantities, lets shorten the ids.
        return uuid.uuid4().hex[:12]

    def _get_response_content_cache_storage_path(self, response: Response) -> Path:
        request = self.get_request(response.request_id)
        unique_but_readable_subdir = f"{url_to_path_dir_name(request.url)}_{request.id}"
        return Path(
            PurePath(self.files_base, unique_but_readable_subdir, response.version)
        )

    def list_requests(
        self,
        group_name: str = None,  # Request.group_name
    ) -> List[Request]:
        all_req: List[Request] = []
        for key in (
            self.db.keys(f"{self.KEY_REQUESTS}:*")
            if not group_name
            else [f"{self.KEY_REQUESTS}:{group_name}"]
        ):
            group_reqs: List[Request] = [
                Request.parse_raw(raw_req) for raw_req in self.db.hgetall(key).values()
            ]
            all_req.extend(group_reqs)
        all_req = sorted(all_req, key=lambda x: x.inital_request_datetime_utc)
        return all_req

    def get_request(self, request_id: str) -> Request:
        # this is expensive... we need to pick up all requets first. maybe a group_name-ids mapping extra hash can improve this, so we only need to pick up the certain group
        return next((req for req in self.list_requests() if req.id == request_id), None)

    def create_request(self, request_in: Request_in) -> Request:
        request: Request = Request.from_request(request_in=request_in)
        request.id = self._generate_id()
        request.cache_configuration.request_id = request.id
        db_key = f"{self.KEY_REQUESTS}:{request.group_name if request.group_name else 'DEFAULT_GROUP'}"
        self.db.hset(db_key, request.id, request.json())
        return request

    def update_request(self, request: Request) -> Request:
        db_key = f"{self.KEY_REQUESTS}:{request.group_name if request.group_name else 'DEFAULT_GROUP'}"
        self.db.hset(db_key, request.id, request.json())
        return request

    def list_responses(
        self, request_id: str, status: str = None, tag: str = None, pinned: bool = None
    ) -> List[Response]:
        db_key = f"{self.KEY_RESPONSES}:{request_id}"
        # one day i will refactor this more readable :) pinky swear
        return sorted(
            [
                res
                for res in [
                    Response.parse_raw(raw_req)
                    for raw_req in self.db.hgetall(db_key).values()
                ]
                if (res.status == status or status is None)
                and (tag is None or tag in res.tags)
                and (
                    pinned is None
                    or (
                        pinned == res.pinned
                        or (
                            pinned and res.pinned_until_utc > datetime.datetime.utcnow()
                        )
                    )
                )
            ],
            key=lambda x: x.version,
            reverse=True,
        )

    def get_response(self, request_id: str = None, version: str = "latest") -> Response:
        """_summary_

        Args:
            request_id (str, optional) Request.id: _description_. Defaults to None.
            version (Response.version, optional) Response.version: _description_. Defaults to "latest".

        Returns:
            Response: _description_
        """
        if version == "latest":
            all = self.list_responses(request_id)
            return all[-1] if all else None

        db_key = f"{self.KEY_RESPONSES}:{request_id}"
        obj = self.db.hget(db_key, version)
        return Response.parse_raw(obj) if obj else None

    def create_response(self, response: Response) -> Response:
        db_key = f"{self.KEY_RESPONSES}:{response.request_id}"
        response.id = self._generate_id()
        self.db.hset(db_key, response.version, response.json())
        return response

    def update_response(self, response: Response) -> Response:
        db_key = f"{self.KEY_RESPONSES}:{response.request_id}"
        self.db.hset(
            db_key,
            response.version,
            response.json(),
        )
        return response

    def delete_response(self, response: Response):
        db_key = f"{self.KEY_RESPONSES}:{response.request_id}"
        self._get_response_content_cache_storage_path(response).unlink(missing_ok=True)
        self.db.hdel(db_key, response.version)

    def add_response_pin_claim(self, pin: ResponsePinClaim):
        """Pinning happens from client side. To prevent any race conditions, clients will only create an application for a pin. The backend will actually set the pin to a response.
        response pin claims are expected to be managed in a queue.
        same for tags."""
        db_key = f"{self.KEY_PIN_CLAIMS}"
        self.db.rpush(db_key, pin.json())

    def fetch_next_response_pin_claim(self) -> ResponsePinClaim:
        """Deliver next pin claim in queue and delete immediately it"""
        db_key = f"{self.KEY_PIN_CLAIMS}"
        obj_raw = self.db.lpop(db_key)
        if obj_raw:
            return ResponsePinClaim.parse_raw(obj_raw)
        return None

    def add_response_tag_claim(self, tag: ResponseTagClaim):
        """Tagging happens from client side. To prevent any race conditions, clients will only create an application for a tag. The backend will actually attach the tag to a response.
        same for tags."""
        db_key = f"{self.KEY_TAG_CLAIMS}"
        self.db.rpush(db_key, tag.json())

    def fetch_next_response_tag_claim(self) -> ResponseTagClaim:
        """Deliver next tag claim in queue and delete immediately it"""
        db_key = f"{self.KEY_TAG_CLAIMS}"
        obj_raw = self.db.lpop(db_key)
        if obj_raw:
            return ResponseTagClaim.parse_raw(obj_raw)
        return None

    ## ↓ CONTENT/FILE HANDLING ↓

    @overload
    async def read_response_content(
        self,
        response: Response,
        as_text: bool = Literal[False],
    ) -> AsyncGenerator[bytes, None]:
        pass

    async def read_response_content(
        self,
        response: Response,
        as_text: bool = Literal[True],
    ) -> AsyncGenerator[str, None]:
        # https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
        # https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi/67497103#67497103
        # why async? https://github.com/tiangolo/fastapi/issues/2302
        # file = "/home/tim/Downloads/tails-amd64-4.16.iso"
        file = self._get_response_content_cache_storage_path(response)
        if as_text:
            for line in open(
                file,
                "rt",
            ).readlines():
                yield line
        else:
            with open(
                file,
                "rb",
            ) as f:
                while True:
                    chunk = f.read(1024)
                    if chunk:
                        yield chunk
                    else:
                        break

    def write_response_content(
        self,
        response: Response,
    ) -> FileIO:
        file = self._get_response_content_cache_storage_path(response)
        file.parent.mkdir(parents=True, exist_ok=True)
        return open(file, "ab")

    def get_response_content_hash(self, response: Response, cached_hash: bool = True):
        if response.content_hash_hex and cached_hash:
            return response.content_hash_hex
        req = self.get_request(request_id=response.request_id)
        hash_func = getattr(hashlib, req.validation_hash_type)
        hash_inst = hash_func()

        async def async_wrapper():
            async for chunk in self.read_response_content(
                response=response, as_text=False
            ):

                hash_inst.update(chunk)

        asyncio.run(async_wrapper())
        response.content_hash_hex = hash_inst.hexdigest()
        self.update_response(response=response)
        return response.content_hash_hex

    def _get_response_target_path(self, response: Response):
        pass
