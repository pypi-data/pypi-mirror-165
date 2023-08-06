import logging

from buffy.buffyserver.backend.storage.interface import StorageInterface
from buffy.buffyserver.api.v1.models import (
    Request,
    Response,
    ResponseTagClaim,
    ResponsePinClaim,
)
import datetime

log = logging.getLogger(__name__)


class TagAndPinManager:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def process_pin_claims(self):
        pin_claim: ResponsePinClaim = self.storage.fetch_next_response_pin_claim()
        while pin_claim:
            res = self.storage.get_response(
                request_id=pin_claim.request_id, version=pin_claim.response_version
            )
            if res:
                log.debug(f"SET PIN {pin_claim}")
                if pin_claim.duration_sec:
                    res.pinned_until_utc = (
                        datetime.datetime.utcnow()
                        - datetime.timedelta(seconds=pin_claim.duration_sec)
                    )
                elif pin_claim.value:
                    res.pinned = True
                elif not pin_claim.value:
                    res.pinned_until_utc = None
                    res.pinned = False
                self.storage.update_response(res)
            # fetch next claim
            pin_claim: ResponsePinClaim = self.storage.fetch_next_response_pin_claim()

    def process_tag_claims(self):
        tag_claim: ResponseTagClaim = self.storage.fetch_next_response_tag_claim()
        while tag_claim:
            res = self.storage.get_response(
                request_id=tag_claim.request_id, version=tag_claim.response_version
            )
            if res:
                log.debug(f"SET TAG {tag_claim}")
                if tag_claim.delete:
                    res.tags.remove(tag_claim.value)
                elif tag_claim.value not in res.tags:
                    res.tags.append(tag_claim.value)
                self.storage.update_response(res)
            # fetch next claim
            tag_claim: ResponseTagClaim = self.storage.fetch_next_response_tag_claim()
