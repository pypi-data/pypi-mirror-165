import logging
from typing import List
from buffy.buffyserver.backend.storage.interface import StorageInterface
from buffy.buffyserver.api.v1.models import Request, Response
import datetime

log = logging.getLogger(__name__)


class StorageJanitor:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def cleanup_storage(self):
        """Remove responses that are too old according to `Request.cache_configuration.max_cached_versions`"""
        for req in self.storage.list_requests():
            self._remove_recent_duplicates(req)
            self._clean_up_request_responses(req)

    def _remove_recent_duplicates(self, request: Request):
        """Check if the recent version changed compared to the previous version and delete it if not"""
        for dup_resp in self.storage.list_responses(
            request_id=request.id, status="duplicate"
        ):
            self._delete_response_if_allowed(dup_resp)

    def _clean_up_request_responses(self, request: Request):
        ready_responses = [
            res
            for res in self.storage.list_responses(request_id=request.id)
            if res.status in ["ready"]
        ]
        if request.cache_configuration.max_cached_versions < len(ready_responses):
            for resp in ready_responses[
                request.cache_configuration.max_cached_versions :
            ]:
                self._delete_response_if_allowed(resp)

    def _delete_response_if_allowed(
        self,
        response: Response,
        previous_response: Response = None,
        next_response: Response = None,
    ) -> bool:
        if (
            response.pinned_until_utc
            and response.pinned_until_utc > datetime.datetime.utcnow()
        ):
            return False
        if response.pinned:
            return False
        # Delete reference in previous version
        if not previous_response and response.previous_version:
            previous_response = self.storage.get_response(response.previous_version)
        if not next_response and response.next_version:
            next_response = self.storage.get_response(response.next_version)
        if previous_response:
            previous_response.next_version = (
                None if not next_response else next_response.version
            )
            self.storage.update_response(previous_response)
        if next_response:
            next_response.previous_version = (
                None if not previous_response else previous_response.version
            )
            self.storage.update_response(next_response)
        self.storage.delete_response(response)
        return True

    def verifiy_storage(self):
        """Remove responses that have issues with their content like unexpected changes or just missing
        This can be a very expensive operation. Use wisely!
        """
        for req in self.storage.list_requests():
            self._verifiy_request_responses(req)

    def _verifiy_request_responses(self, request: Request):
        for resp in [
            res
            for res in self.storage.list_responses(request_id=request.id)
            if res.status in ["ready"]
        ]:
            old_hash = resp.content_hash_hex
            try:
                current_hash = self.storage.get_response_content_hash(
                    resp, cached_hash=False
                )
            except FileNotFoundError:
                # file is missing. we have a garbage response here. lets just delete it
                log.warning(
                    f"Request.id: '{request.id}' Response.id: '{resp.id}' -> Error during validation hashing. Response will be deleted"
                )
                self.storage.delete_response(resp)
                # go to next response
                continue
            if old_hash != current_hash:
                # the file changed. this means from our perspective the file is corrupt
                log.warning(
                    f"Request.id: '{request.id}' Response.id: '{resp.id}' -> Response content changed unexpected. Response will be deleted"
                )
                self.storage.delete_response(resp)
