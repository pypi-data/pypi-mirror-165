from io import TextIOWrapper, FileIO
from typing import (
    Dict,
    List,
    overload,
    Generator,
    Literal,
    AsyncGenerator,
)
import redis
from pathlib import Path
import hashlib


from buffy.buffyserver.api.v1.models import (
    Response,
    Request,
    Request_in,
    RequestCacheConfiguration,
    ResponsePinClaim,
    ResponseTagClaim,
)
from buffy.tools.utils import url_to_path_dir_name

"""Backend brainstorming notes

* Store large bynaries files
* provide hash per file

"""


class StorageInterface:
    def __init__(self, file_storage_dir: Path, config=None):
        raise NotImplementedError

    def test_connection(self) -> bool:
        raise NotImplementedError

    def list_requests(
        self,
        group_name: str = None,  # Request.group_name
    ) -> List[Request]:
        """List all requests from (index 0) oldest to newest

        Args:
            group_name (str, optional): _description_. Defaults to None.

        Returns:
            List[Request]:
        """
        raise NotImplementedError

    def get_request(self, request_id: str) -> Request:
        """Return a request queried by its id. If not found return None

        Args:
            request_id (str): _description_

        Returns:
            Request: _description_
        """

        raise NotImplementedError

    def create_request(self, request: Request) -> Request:

        raise NotImplementedError

    def update_request(self, request: Request) -> Request:
        raise NotImplementedError

    def list_responses(
        self, request_id: str, status: str = None, tag: str = None, pinned: bool = None
    ) -> List[Response]:
        """List Responses to a certain request. Must be sorted from (index 0) newest/freshest response to oldest

        Args:
            request_id (str): _description_
            status (str, optional): _description_. Defaults to None.
            tag (str, optional): _description_. Defaults to None.
            pinned (bool, optional): _description_. Defaults to None.

        Raises:
            NotImplementedError: _description_

        Returns:
            List[Response]: _description_
        """
        raise NotImplementedError

    def create_response(self, response: Response) -> Response:
        raise NotImplementedError

    def update_response(self, response: Response) -> Response:
        raise NotImplementedError

    def get_response(self, request_id: str = None, version: str = "latest") -> Response:
        """Return a response by its request id and version name. If reponse id and/or version name not exists return None

        Args:
            request_id (str, optional): _description_. Defaults to None.
            version (str, optional): _description_. Defaults to "latest".

        Raises:
            NotImplementedError: _description_

        Returns:
            Response: _description_
        """
        raise NotImplementedError

    def update_response(self, response: Response):
        raise NotImplementedError

    def delete_response(self, response: Response):
        raise NotImplementedError

    def add_response_pin_claim(self, pin: ResponsePinClaim):
        """Pinning happens from client side. To prevent any race conditions, clients will only create an application for a pin. The backend will actually set the pin to a response.
        response pin claims are expected to be managed in a queue.
        same for tags."""
        raise NotImplementedError

    def fetch_next_response_pin_claim(self) -> ResponsePinClaim:
        """Deliver next pin claim in queue and delete immediately it"""
        raise NotImplementedError

    def add_response_tag_claim(self, tag: ResponseTagClaim):
        """Tagging happens from client side. To prevent any race conditions, clients will only create an application for a tag. The backend will actually attach the tag to a response.
        same for tags."""
        raise NotImplementedError

    def fetch_next_response_tag_claim(self) -> ResponseTagClaim:
        """Deliver next tag claim in queue and delete immediately it"""
        raise NotImplementedError

    ## ↓ CONTENT/FILE HANDLING ↓

    @overload
    async def read_response_content(
        self,
        response: Response,
        as_text: bool = Literal[False],
    ) -> AsyncGenerator[bytes, None]:
        raise NotImplementedError

    async def read_response_content(
        self,
        response: Response,
        as_text: bool = Literal[True],
    ) -> AsyncGenerator[str, None]:

        raise NotImplementedError

    def write_response_content(
        self,
        response: Response,
    ) -> FileIO:
        raise NotImplementedError

    def update_response_content_writing(
        self,
        response: Response,
    ):
        raise NotImplementedError

    def close_response_content_writing(self):
        raise NotImplementedError

    def get_response_content_hash(self, response: Response, cached_hash: bool = True):
        raise NotImplementedError
