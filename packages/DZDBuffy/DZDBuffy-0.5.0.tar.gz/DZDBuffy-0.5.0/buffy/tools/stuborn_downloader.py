import os
from typing import Dict, Callable, Union
from io import FileIO, BytesIO
import requests
from requests.structures import CaseInsensitiveDict
from email.utils import parsedate_to_datetime
from pathlib import Path, PurePath
from urllib.parse import urlparse
import mimetypes
import time
import logging
import hashlib

# rename to avoid confusions with requests.Response and requests.Request

from buffy.buffyserver.api.v1.models import (
    Request_in as BuffyRequest,
    ResponseContentAttributes,
    ResponseDownloadStats,
)
from buffy.tools.utils import HttpHeaderContentDispositionParser

log = logging.getLogger(__name__)


class StubornDownloader:
    FILE_EXTENSION_FOR_PARTIAL_DOWNLOADED_FILE: str = ".part"
    HTTP_METHOD_MAP: Dict[str, Callable] = {
        "get": requests.get,
        "put": requests.put,
        "post": requests.post,
    }
    # https://stackoverflow.com/questions/23369625/ideal-chunk-size-for-python-requests
    CHUNK_SIZE: int = 65536
    DEFAULT_WAIT_TIME_SEC_ON_429: int = 2

    MAX_DOWNLOAD_ATTEMPTS: int = 6
    CLOSE_FILE_OBJ: bool = True
    # important status codes
    # 429 - Too Many Requests - https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429
    #   Solution: A "Retry-After" header might be included to this response indicating how long to wait before making a new request.
    def __init__(self, request: "BuffyRequest"):
        self.request = request
        self.byte_position = 0
        self.overwrite_filename = None
        self.fallback_filename = "download"
        self.call_report_hook_every_n_chunks_downloaded = 10
        self.accept_ranges: bool = None
        self.response_header_fields: CaseInsensitiveDict = None
        self.status: ResponseDownloadStats = None
        self.finished: bool = False
        self.hash: str = None

        self._status_updates(
            ResponseDownloadStats(
                downloaded_bytes=0,
                avg_bytes_per_sec=None,
                download_running_duration_sec=None,
                download_start_time_unix_ts=None,
                total_bytes_to_download=None,
                state="init",
            )
        )

    def hook_status_updates(self, status: ResponseDownloadStats):
        # mb_per_sec: float = round(status.avg_bytes_per_sec / 1048576, 2)
        pass

    def get_response_content_attrs(
        self, cached_only: bool = False
    ) -> ResponseContentAttributes:
        if not self.response_header_fields and not cached_only:
            response: requests.Response = None
            try:
                if self.request.http_method == "get":
                    response: requests.Response = requests.head(
                        self.request.url,
                        params=self.request.http_query_params,
                        headers=self.request.http_header_fields,
                        timeout=1,
                    )
                    self.response_header_fields = response.headers
                    response.raise_for_status()
                else:
                    raise
            except:
                # webserver does not support "head" calls or we have no 'get'. Then just pretend a download
                try:
                    response: requests.Response = self.HTTP_METHOD_MAP[
                        self.request.http_method
                    ](
                        self.request.url,
                        params=self.request.http_query_params,
                        headers=self.request.http_header_fields,
                        stream=True,
                        timeout=1,
                    )
                    self.response_header_fields = response.headers
                    response.close()
                except (
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError,
                ):
                    if response:
                        response.close()
                    return ResponseContentAttributes()
        elif not self.response_header_fields and cached_only:
            return ResponseContentAttributes()
        response_content_attrs = ResponseContentAttributes(
            etag=self.response_header_fields.get("ETag", None),
            size_in_bytes=self.response_header_fields.get("Content-Length", None),
            filename=self._guess_filename(
                headers=self.response_header_fields,
                url=self.request.url,
                fallback_filename=None,
            ),
            content_disposition=self.response_header_fields.get("Content-Disposition"),
        )
        _media_type = self.response_header_fields.get("Content-Type", None)
        if _media_type:
            response_content_attrs.media_type = _media_type.split(";")[0]
        _last_modified = self.response_header_fields.get("Last-Modified", None)
        if _last_modified:
            response_content_attrs.last_modified_datetime_utc = parsedate_to_datetime(
                _last_modified
            )
        response_content_attrs = self._correct_content_length(response_content_attrs)
        return response_content_attrs

    def _correct_content_length(
        self, response_content_attrs: ResponseContentAttributes
    ) -> ResponseContentAttributes:
        if self.finished:
            if response_content_attrs.content_size_bytes is not None and (
                response_content_attrs.content_size_bytes
                != self.status.downloaded_bytes
            ):
                log.warning(
                    f"""'Content-length' for file '{self.request.url}' was announced as '{response_content_attrs.content_size_bytes}' bytes,  but actually is {self.status.downloaded_bytes} bytes.
                    Buffy downloader will correct this information for the clients response header."""
                )
            response_content_attrs.content_size_bytes = self.status.downloaded_bytes
        return response_content_attrs

    def download(
        self,
        target_dir: Union[Path, str] = None,
        file_obj: Union[FileIO, BytesIO] = None,
    ) -> Union[PurePath, FileIO]:
        if (target_dir and file_obj) or (not target_dir and not file_obj):
            err_msg = f"Expected 'target_dir' OR 'file_obj' for storing download. Got both or none for remote file '{self.request.url}'.\n'target_dir'='{target_dir}'\n'file_obj'={file_obj}\n"
            log.error(err_msg)
            raise ValueError(err_msg)
        elif file_obj and isinstance(file_obj, FileIO):
            if file_obj.mode != "ab":
                err_msg = f"Expected file_obj to be in mode 'ab'. got {file_obj.mode}"
                raise ValueError(err_msg)
        result: Union[PurePath, FileIO] = None
        download_attempts: int = 0
        while not self.finished:
            download_attempts += 1
            try:
                if self.request.validation_hash_type:
                    self._hash_func = getattr(
                        hashlib, self.request.validation_hash_type
                    )()
                else:
                    self._hash_func

                result = self._download(
                    target_dir=target_dir,
                    file_obj=file_obj,
                    start_at_byte=self.byte_position if self.accept_ranges else 0,
                )
                self.finished = True
                self.status.state = "finished"
                self._status_updates(self.status)
                if self._hash_func:
                    self.hash = self._hash_func.hexdigest()

            except requests.exceptions.RequestException as e:
                # we only want to catch http/network/requests errors. other errors are propaply not solved by retrying
                if download_attempts >= self.MAX_DOWNLOAD_ATTEMPTS:
                    self.status.state = "failed"
                    self._status_updates(self.status)
                    raise e
        return result

    def _download(
        self,
        target_dir: Union[Path, str],
        file_obj: FileIO,
        start_at_byte: int = 0,
    ) -> PurePath:

        request_header_fields = CaseInsensitiveDict(self.request.http_header_fields)
        response_complete: bool = False

        while not response_complete:
            response: requests.Response = self.HTTP_METHOD_MAP[
                self.request.http_method
            ](
                self.request.url,
                params=self.request.http_query_params,
                headers=request_header_fields,
                stream=True,
                timeout=60,
            )
            response_complete = True
            self.accept_ranges = (
                True
                if response.headers.get("Accept-Ranges", False) == "bytes"
                else False
            )
            if response.status_code == 429:
                # 429 Too Many Requests # wait for xxx seconds
                retry_after_sec = int(response.headers.get("Retry-After", None))
                retry_after_sec = (
                    self.DEFAULT_WAIT_TIME_SEC_ON_429
                    if not retry_after_sec
                    else retry_after_sec
                )
                log.warning(f"Too many requests. wait {retry_after_sec} seconds...")
                response_complete = False
                time.sleep(int(retry_after_sec))

            elif not self.accept_ranges and start_at_byte != 0:
                raise ValueError(
                    f"'Accept-Ranges' is false but 'start_at_byte' required by caller. Server does not provide resuming downloads or partial downloads."
                )
            elif (
                self.accept_ranges
                and start_at_byte != 0
                and request_header_fields.get("Range", None) is None
            ):
                # this is a resumed download. We request to not download the whole file but start a specific byte position via the header field Range
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
                request_header_fields["Range"] = f"bytes={start_at_byte}"
                response_complete = False

        response.raise_for_status()
        self.response_header_fields = response.headers
        total_length_bytes = response.headers.get("Content-Length", None)
        if self.overwrite_filename:
            file_name = self.overwrite_filename
        else:
            file_name = self._guess_filename(
                headers=response.headers,
                url=self.request.url,
                fallback_filename=self.fallback_filename,
            )

        if not file_obj:
            # caller wants us to manage file target
            if not target_dir:
                target_dir = "./"
            target_path = PurePath(target_dir, file_name)

            temp_target_path = PurePath(
                str(target_path) + self.FILE_EXTENSION_FOR_PARTIAL_DOWNLOADED_FILE
            )
            write_target = open(temp_target_path, "ab")
        else:
            write_target = file_obj

        if start_at_byte == 0:
            # reset any previous download attempts
            write_target.seek(0)
            write_target.truncate()
        i: int = 0
        start_time = time.time()
        # START DOWNLOAD
        self._status_updates(
            ResponseDownloadStats(
                downloaded_bytes=self.byte_position,
                avg_bytes_per_sec=0,
                download_running_duration_sec=0,
                download_start_time_unix_ts=start_time,
                total_bytes_to_download=total_length_bytes,
                state="downloading",
            )
        )
        for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
            if chunk:
                write_target.write(chunk)
                self.byte_position += len(chunk)
                if self._hash_func:
                    self._hash_func.update(chunk)
                if i % self.call_report_hook_every_n_chunks_downloaded == 0:
                    current_time = time.time()
                    self._status_updates(
                        ResponseDownloadStats(
                            downloaded_bytes=self.byte_position,
                            avg_bytes_per_sec=self.byte_position
                            / (current_time - start_time),
                            download_running_duration_sec=current_time - start_time,
                            download_start_time_unix_ts=start_time,
                            total_bytes_to_download=total_length_bytes,
                            state="downloading",
                        )
                    )

            i += 1
        current_time = time.time()
        self._status_updates(
            ResponseDownloadStats(
                downloaded_bytes=self.byte_position,
                avg_bytes_per_sec=self.byte_position / (current_time - start_time),
                download_running_duration_sec=current_time - start_time,
                download_start_time_unix_ts=start_time,
                total_bytes_to_download=total_length_bytes,
                state="downloading",
            )
        )
        response.close()
        if (file_obj and self.CLOSE_FILE_OBJ) or not file_obj:
            write_target.close()
        if not file_obj:
            # lets move our temp content to callers desired target
            try:
                os.remove(target_path)
            except FileNotFoundError:
                pass
            os.rename(temp_target_path, target_path)
        return target_path if not file_obj else file_obj

    def _guess_filename(
        self, headers: CaseInsensitiveDict, url: str, fallback_filename: str = None
    ) -> str:
        # FILENAME VIA CD
        # try to get filename the offical way via content-disposition
        try:
            content_disposition = HttpHeaderContentDispositionParser(
                headers.get("content-disposition")
            )
        except ValueError as err:
            content_disposition = None
            log.error(err)
        if content_disposition and content_disposition.filename_unsafe:
            return content_disposition.filename
        # if content_disposition and content_disposition.type in ["inline", "form-data"]:
        #    return None

        # ALTERNATIVES METHODS
        ## FILE EXTENSION
        ## first lets try to get the file extension
        ext: str = None
        content_type: str = headers.get("Content-Type", None)
        if content_type:
            content_type = content_type.split(";")[0]
        if content_type:
            # try to get it via Content-Type header
            ext = mimetypes.guess_extension(content_type)
            ext = ext.replace(".", "") if ext else None
        ## FILENAME VIA URL
        ## try to pick it out of the url
        filename = (
            PurePath(urlparse(url).path).name
            if PurePath(urlparse(url).path).suffix
            else None
        )
        if filename:
            return filename
        ## fallback to default filename with a last try to guess the filename type and at least generate a correct filename extension
        if fallback_filename and ext:
            return fallback_filename + "." + ext
        if ext:
            return self.fallback_filename + "." + ext
        return self.fallback_filename

    def _status_updates(self, status: ResponseDownloadStats):
        # mb_per_sec: float = round(avg_speed_bytes_per_sec / 1048576, 2)
        self.status = status
        # we copy the object as its not intended to mutate the status from extern
        self.hook_status_updates(ResponseDownloadStats(**dict(status)))
