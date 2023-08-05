from functools import cache
from genericpath import isfile
from typing import Dict, Literal, List, Optional, Union, Iterator, Annotated
import logging
from xml.dom import ValidationErr
from buffy.buffyserver.api.v1.models import (
    Request as ApiRequest,
    Request_in as ApiRequest_in,
    Response as ApiResponse,
    ResponseDownloadStats,
    ResponsePinClaim,
    ResponseTagClaim,
)
from buffy.buffyserver.api.v1.models import RequestCacheConfiguration
from buffy.buffyserver.api.v1.models_recaching_strategies import ReCachingStrategy
from pathlib import Path, PurePath
from buffy.tools.stuborn_downloader import StubornDownloader
import requests
from io import FileIO
import tempfile
import threading
import time
from pydantic import parse_raw_as
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse


log = logging.getLogger(__name__)


class BuffyServerError(Exception):
    pass


class BuffyCacheEmptyError(Exception):
    pass


class BuffyPyClient:
    """Python client to abstract communication with the Buffy server REST API"""

    buffy_server_timeout_sec = 5

    class Request:
        """Return object of [`Buffy.BuffyPyClient.create_request()`](/BuffyPyClient/#buffy.buffypyclient.buffypyclient.BuffyPyClient.create_request)

        Args:
            force_version (str, optional): The size of byte chunks you want to iterate. Defaults to 64 kibibyte.

        """

        def __init__(self, request: ApiRequest_in, client: "BuffyPyClient"):
            self._client = client
            self._api_request_in: ApiRequest_in = request
            self._api_request: ApiRequest = None
            self._api_response: ApiResponse = None
            self._use_local_download: bool = False
            self._local_downloader: StubornDownloader = None
            self._local_temp_file: FileIO = None

            self.force_version: str = None
            """if you want to have a certain version of all cached responses, set `force_version`. To list all available versions use """
            self.prefere_version: str = None
            self.prefere_tag: str = None
            """If a response version with this tag is available it will be preferred to be served to the client."""
            self.prefere_pinned: bool = False
            self.prefere_cached_instead_of_waiting: bool = False
            self._response_query_filter_attr_priorisation: List[str] = [
                "pinned",
                "tag",
                "status",
            ]
            """When prefering tag and pinned and status of a response at the same time, which constraint should be dropped first"""
            self.force_pinned: bool = None
            self.force_version: str = None
            self.force_tag: str = None
            self.fallback_to_older_version = True
            self.buffy_server_http_headers: Dict = {}
            """Header fields send to the Buffy server API. This can be used e.g. if Buffy is behind a auth reverse proxy"""
            self.buffy_server_http_auth: HTTPBasicAuth = None
            """HTTP Auth fields send to the Buffy server API. This can be used e.g. if Buffy is behind a auth reverse proxy"""

        @property
        def cache_configuration(self) -> RequestCacheConfiguration:
            if not self._api_request:
                return self._api_request_in.cache_configuration
            else:
                return self._api_request.cache_configuration

        @cache_configuration.setter
        def cache_configuration(self, cache_configuration: RequestCacheConfiguration):
            if not self._api_request:
                self._api_request_in.cache_configuration = cache_configuration
            else:
                self._api_request.cache_configuration = cache_configuration
                try:
                    res = requests.put(
                        f"{self._client.api_url}/request/{self._api_request.id}/cache-config",
                        data=cache_configuration.json()
                        if cache_configuration
                        else None,
                        timeout=self._client.buffy_server_timeout_sec,
                        headers=self.buffy_server_http_headers,
                        auth=self.buffy_server_http_auth,
                    )
                    res.raise_for_status()
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout,
                ) as e:
                    log.warning(
                        f"Can not reach BuffyServer @ '{self._client.api_url}'. Cache configuration is not updated on server side."
                    )

        @property
        def next_version(self):
            """Query the server if there is a newer version available"""
            if self._api_response and self._api_response.next_version:
                return self._api_response.next_version

        @property
        def previous_version(self):
            """Query the server if there is a newer version available"""
            if self._api_response and self._api_response.previous_version:
                return self._api_response.previous_version

        @property
        def response_version(self):
            if self._api_response:
                return self._api_response.version
            log.warning(
                "You tried to get a response version, before BuffyPyClient could ask the Buffy Server for the recommended version"
            )

        def order(
            self,
            prefer_cached: bool = True,
            prefer_pinned: bool = None,
            prefer_version: str = None,
            prefer_tag: str = None,
            force_pinned: bool = None,
            force_version: str = None,
            force_tag: str = None,
        ):
            """Send the request to the Buffy server.
            When calling [`Buffy.BuffyPyClient.create_request()`](/BuffyPyClient/#buffy.buffypyclient.buffypyclient.BuffyPyClient.create_request) `order` will be called automaticly.
            If you want determine the moment when the Buffy server is reached manually, call `create_request()' with `hold_request_order=True` and use this function to call the Buffy server whenever you are ready


            Args:
                prefer_cached (bool, optional): _description_. Defaults to True.
                prefer_pinned (bool, optional): _description_. Defaults to None.
                prefer_version (str, optional): _description_. Defaults to None.
                prefer_tag (str, optional): _description_. Defaults to None.
                force_pinned (bool, optional): _description_. Defaults to None.
                force_version (str, optional): _description_. Defaults to None.
                force_tag (str, optional): _description_. Defaults to None.

            Raises:
                SystemError: _description_
                e: _description_
            """
            self.prefere_cached_instead_of_waiting = prefer_cached
            self.prefere_pinned = prefer_pinned
            self.prefer_version = prefer_version
            self.prefer_tag = prefer_tag
            self.force_pinned = force_pinned
            self.force_version = force_version
            self.force_tag = force_tag
            try:
                res: requests.Response = requests.put(
                    f"{self._client.api_url}/request/",
                    data=self._api_request_in.json(),
                    timeout=self._client.buffy_server_timeout_sec,
                    verify=False,
                    headers=self._client.http_headers,
                    auth=self._client.http_auth,
                )
                res.raise_for_status()
            except requests.exceptions.ConnectionError as e:
                if self._client.local_download_fallback:
                    log.warning(
                        f"Can not reach BuffyServer @ '{self._client.api_url}'. Fallback to local uncached download."
                    )
                    self._use_local_download = True
                    self.download_thread = threading.Thread(
                        target=self._run_local_download
                    )
                    self.download_thread.start()
                    t = time.time()
                    while self._local_downloader is None:
                        timeout = 2
                        # Wait for local download to initialize. This needs to be done to prevents racing cond
                        if time.time() - t > timeout:
                            raise SystemError(
                                "Could not initialize local downloader..."
                            )
                        time.sleep(0.1)
                    return
                else:
                    log.error(f"Can not reach BuffyServer @ '{self._client.api_url}'.")
                    raise e
            except:
                log.error(f"Request data: {self._api_request_in.json()}")
                if hasattr(res, "content"):
                    log.error(f"Response content {res.content}")
                raise

            self._api_request: ApiRequest = ApiRequest.parse_raw(res.content)
            if (
                self._api_request_in.cache_configuration
                and self._api_request_in.cache_configuration
                != self._api_request.cache_configuration
            ):
                # the caller updated the cache config. lets update on server side
                self.cache_configuration = self._api_request_in.cache_configuration
            self._wait_for_request_registration()

        def download_response_content(self, chunk_size: int = 65536) -> Iterator[bytes]:
            """Stream/Iterate through the response content delivered by the Buffy server.

            **example use**
            ```python
            from buffy.buffypyclient import BuffyPyClient
            c = BuffyPyClient()
            req = c.create_request(
                url="https://meowfacts.herokuapp.com/"
            )
            cat_fact = ""
            for chunk in req.download_response_content():
                cat_fact += chunk.decode("utf-8")
            print(json.loads(cat_fact))
            ```

            Args:
            Args:
                chunk_size (int, optional): The size of byte chunks you want to iterate. Defaults to 64 kibibyte.

                Iterator[bytes]: The reponse content in byte chunks
            """
            self._wait_for_response_completion()
            if not self._use_local_download:
                response = self._find_response()
                download_url = (
                    f"{self._client.api_url}/{response.content_download_path}"
                )
                with requests.get(
                    download_url,
                    headers=self.buffy_server_http_headers,
                    auth=self.buffy_server_http_auth,
                    stream=True,
                ) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        yield chunk
            else:
                self._local_temp_file.seek(0)
                while True:
                    chunk = self._local_temp_file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        def download_response_content_to(
            self, target: Union[str, Path, FileIO] = None, dir: Union[str, Path] = None
        ) -> Path:
            """Download the response content delivered by the Buffy server.

            **example use**
            ```python
            from buffy.buffypyclient import BuffyPyClient
            c = BuffyPyClient()
            req = c.create_request(url="https://www.foaas.com/awesome/:tim")
            content_path = req.download_response_content_to(dir="/tmp")
            print(content_path)
            # > `/tmp/download.html`
            ```

            Args:
                target (Union[str, Path, FileIO], optional): Download target as a file like object \
                    or a file path.
                dir (Union[str, Path], optional): Alternative to `target`. \
                    A directory as download path. Buffy tries to evaluate the filename \ 
                    but will fallback to `download`. Defaults to None.

            Returns:
                Path: The final path of the downloaded content.
            """
            file = target
            if dir and target:
                raise ValueError("Use target or dir as filesink not both")
            if dir:
                target = Path(PurePath(dir, self.get_filename()))
            if isinstance(target, str):
                target = Path(target)
            if isinstance(target, Path):
                file = open(target, "wb")
            for chunk in self.download_response_content():
                file.write(chunk)
            if isinstance(target, (str, Path)):
                # We only close the file object if we created ourselves
                file.close()
            return target

        def list_cached_response_versions(
            self,
            status: Union[
                Literal["wait", "in_progress", "ready", "duplicate", "failed"], None
            ] = "ready",
            skip: int = 0,
            limit: Union[int, None] = 10,
        ) -> List[ApiResponse]:
            """Get a list of all cached responses of the request

            ```python
            from buffy.buffypyclient import BuffyPyClient
            c = BuffyPyClient()
            req = c.create_request(url="https://www.foaas.com/awesome/:tim")
            cached_responses = req.list_cached_versions()
            for resp in cached_responses:
                print(resp.id)
            ```

            Returns:
                List[ApiResponse]: _description_
            """
            response_url: str = (
                f"{self._client.api_url}/request/{self._api_request.id}/response"
            )
            response_raw = requests.get(
                response_url,
                headers=self.buffy_server_http_headers,
                auth=self.buffy_server_http_auth,
                params={"status": status, "skip": skip, "limit": limit},
            ).content
            return parse_raw_as(List[ApiResponse], response_raw)

        def get_filename(self, fallback_filename="download") -> Union[str, None]:
            """Try to evaluate the filename of the response content.
            This is based on HTTP headers like \
                [`Content-Disposition`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition) and \
                [`Content-Type`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type)

            Args:
                fallback_filename (str, optional): A filename to fallback if `get_filename` can not evaluate a filename. Defaults to "download".

            Returns:
                The filename as string or `None` if no filename cloud be evaluated and `fallback_filename` is set to `None`
            """
            self._wait_for_response_content_attributes()

            if self._use_local_download:
                filename = self._local_downloader.get_response_content_attrs(
                    cached_only=True
                ).filename
            else:
                filename = self._find_response().content_attributes.filename
            return filename if filename else fallback_filename

        def pin(
            self,
            value: bool = True,
            response_version: str = None,
            duration_sec: int = None,
        ) -> str:
            """Pin the current response version.
            Pinning means telling the server not to delete the response version while gargabe collecting.
            If you have a response version that works with your code you can pin it and reuse it as a fallback, if newer reponse version failed with your code
            To unpin a response set `value=False`

            Args:
                response_version (str, optional): If not defined the current response version will be pinned. alternativly you can pin any other version by providing its name
                duration_sec (int, optional): If you only want to pin a version temporary, define a time span in seconds

            Returns:
                str: Version name of the pinned response.
            """

            if not response_version:
                if not self._api_response:
                    raise ValueError(
                        "BuffyPyClient can not pin any response version. No `response_version` provided and no response from Buffy server ordered yet."
                    )
                response_version = self._api_response.version
            pin = ResponsePinClaim(value=value, duration_sec=duration_sec)
            api_url = f"{self._client.api_url}/request/{self._api_request.id}/response/v/{response_version}/pin"
            requests.put(
                api_url,
                headers=self.buffy_server_http_headers,
                auth=self.buffy_server_http_auth,
                data=pin.json(),
            )

        def unpin(self, response_version: str = None):
            self.pin(response_version=response_version, value=False)

        def tag(
            self,
            tag: str,
            response_version: str = None,
            remove_tag: bool = False,
        ) -> str:
            """Tag the current response version.
            You can attach user defined tags to cached responses. This way you can organize and search your responses.

            A valid tag is any alphanummeric string without any whitespaces and minimal 3 chars and maximal 64 chars

            Args:
                tag (str): If not defined the current response version will be pinned. alternativly you can pin any other version by providing its name
                response_version (str, optional): If not defined the current response version will be tagged. alternativly you can tag any other version by providing its name
                remove_tag (bool): If `True` the tag will be removed if existent

            Returns:
                str: Version name of the pinned response.
            """

            if not response_version:
                if not self._api_response:
                    raise ValueError(
                        "BuffyPyClient can not tag any response version. No `response_version` provided and no response from Buffy server ordered yet."
                    )
                response_version = self._api_response.version
            tag_claim = ResponseTagClaim(
                response_version=response_version, value=tag, delete=remove_tag
            )
            api_url = f"{self._client.api_url}/request/{self._api_request.id}/response/v/{response_version}/tag"
            requests.put(
                api_url,
                headers=self.buffy_server_http_headers,
                auth=self.buffy_server_http_auth,
                data=tag_claim.json(),
            )

        def __del__(self):
            if self._local_temp_file and not self._local_temp_file.closed:
                self._local_temp_file.close()

        def _is_request_registered(self) -> bool:
            res: requests.Response = requests.get(
                f"{self._client.api_url}/request/{self._api_request.id}/status/{self._api_request.request_timestamp}",
                headers=self.buffy_server_http_headers,
                auth=self.buffy_server_http_auth,
            )
            res.raise_for_status()

            if res.status_code == 102:
                return False
            elif res.status_code == 200:
                return True

        def _get_download_stats(
            self, response: ApiResponse = None
        ) -> ResponseDownloadStats:
            if self._use_local_download:
                return self._local_downloader.status
            else:
                # update response status
                response_url: str = f"{self._client.api_url}/request/{self._api_request.id}/response/v/{response.version if response else self._find_response().version}"
                response_raw = requests.get(
                    response_url,
                    headers=self.buffy_server_http_headers,
                    auth=self.buffy_server_http_auth,
                ).content
                self._api_response = ApiResponse.parse_raw(response_raw)
                return self._api_response.download_stats

        def _run_local_download(self):
            # in extra thread option?
            self._local_downloader = StubornDownloader(self._api_request_in)
            self._local_downloader.CLOSE_FILE_OBJ = False
            self._local_temp_file = tempfile.TemporaryFile()
            self._local_downloader.download(file_obj=self._local_temp_file)

        def _wait_for_local_download(self):
            raise NotImplementedError()

        def _wait_for_request_registration(self):
            """Wait until the request is processed by the backend and a possible response had arrived in the database"""
            if self._api_request is None:
                raise ValidationErr(
                    f"Request for '{self._api_request_in.url}' must be started with method 'BuffyPyClient.Request.order() first'"
                )
            while not self._is_request_registered():
                time.sleep(0.3)

        def _wait_for_response_completion(
            self, render_progressbar: bool = False, timeout_sec: int = None
        ):
            if render_progressbar:
                raise NotImplementedError()
            is_complete: bool = False
            start_time = time.time()
            while not is_complete:
                stats: ResponseDownloadStats = self._get_download_stats()
                if not self._use_local_download and self._api_response.status in [
                    "wait"
                ]:
                    # the download has not started yet. lets wait another server tick
                    pass
                elif stats.state == "finished":
                    return
                if timeout_sec and time.time() - start_time > timeout_sec:
                    raise TimeoutError(
                        f"Client timeout while waiting for Response '{self._api_request.url}'"
                    )
                time.sleep(0.3)

        def _wait_for_response_content_attributes(self, timeout_sec: int = None):
            if timeout_sec:
                raise NotImplementedError()
            if self._use_local_download:
                self._local_downloader.get_response_content_attrs()
            else:
                is_complete: bool = False
                while not is_complete:
                    resp = self._find_response()

                    if resp.content_attributes.filename is not None:
                        return
                    time.sleep(0.3)

        def _find_response(self, override_prefere_version: str = None) -> ApiResponse:
            """Try to find a matching response stored and/or processed in Buffy server to serve the client

            Todo: Simplify logic. Its a mess atm

            Args:
                override_prefere_version (str, optional): _description_. Defaults to None.

            Raises:
                ValueError: _description_
                BuffyCacheEmptyError: _description_

            Returns:
                ApiResponse: _description_
            """
            # Check if we already called _find_response() and found a response
            if self._api_response:
                # update state of reponse
                self._get_download_stats(response=self._api_response)
                if self._api_response.status not in ["failed", "duplicate"]:
                    # if the state of the reponse is healthy we can serve it.
                    # otherwise we continue the function and need to find another one
                    return self._api_response

            if self._use_local_download:
                # we could not reach the buffy server and started local download. nothing todo here.
                return None
            if self._api_request is None:
                # There was no request ordered (`BuffyPyClient.Request.order()`) until now.
                # We have no connection to the buffy server yet and therefore cant find a cached response
                raise ValueError(
                    f"Cant query matching response for Request '{self._api_request_in.url}'. The request must be ordered with method `BuffyPyClient.Request.order()` first"
                )

            prefer_version = (
                override_prefere_version
                if override_prefere_version
                else self.prefere_version
            )

            def query_response(url, params: Dict = None) -> ApiResponse:
                if not params:
                    params = {}
                print("QUERY", url, params)
                response_raw = requests.get(
                    url,
                    headers=self.buffy_server_http_headers,
                    auth=self.buffy_server_http_auth,
                    params=params,
                )

                if (
                    response_raw.status_code in [404, 204]
                    or response_raw.content is None
                ):
                    return None
                response_raw.raise_for_status()
                if response_raw.content:
                    return ApiResponse.parse_raw(response_raw.content)

            response: ApiResponse = None
            # caller wants a certain version
            if self.force_version or prefer_version:
                response_get_url: str = f"{self._client.api_url}/request/{self._api_request.id}/response/v/{self.force_version if self.force_version else prefer_version}"
                response = query_response(response_get_url)
                if response is None and self.force_version:
                    raise ValueError(
                        f"Forced version {self.force_version} could not be found"
                    )
            if not response and (self.force_pinned or self.force_tag):
                response_get_url: str = f"{self._client.api_url}/request/{self._api_request.id}/response/latest"
                filter_params = {
                    "tag": self.force_tag,
                    "pinned": self.force_pinned,
                }
                response = query_response(response_get_url, filter_params)
                if response is None:
                    raise ValueError(
                        f"Forced {'Tagged' + self.force_tag if self.force_tag else ''} {'and' if self.force_tag and self.force_pinned else ''} {'pinned' if self.force_pinned else ''} version could not be found"
                    )
            # caller wants any latest version, maybe with some prefered attributes
            status = "ready" if self.prefere_cached_instead_of_waiting else None
            filter_params = {
                "tag": self.prefer_tag,
                "pinned": self.prefere_pinned,
                "status": status,
            }
            i = 0
            while not response:
                response_get_url: str = f"{self._client.api_url}/request/{self._api_request.id}/response/latest"

                response = query_response(response_get_url, filter_params)
                if not filter_params:
                    # There are no query filters anymore we can drop
                    break
                # drop limitations to query a wider range of responses
                del filter_params[self._response_query_filter_attr_priorisation[i]]
                i += 1
            if response is None or response.status == "failed":
                raise BuffyCacheEmptyError(
                    f"Current response for request '{self._api_request.url}' failed to download and no previous version is cached. sorry!"
                )
            if response.status == "duplicate":
                response = self._find_response(
                    override_prefere_version=response.previous_version
                )
            return response

    def __init__(
        self,
        url: str = None,
        host: str = None,
        port: int = 8008,
        base_path: str = None,
        group_name: str = None,
        api_version: Literal["v1"] = "v1",
        ssl: bool = False,
        http_auth: HTTPBasicAuth = None,
        http_headers: Dict = {},
        local_download_fallback: bool = True,
    ):
        self.http_auth = None
        if not host and not url:
            host = "localhost"
        if host:
            self.ssl = ssl
            self.host = host
            self.port = port
            self.base_path = base_path
        elif url:
            parsed_url = urlparse(url)
            self.ssl = True if parsed_url.scheme in ["https", None] else False
            self.host = parsed_url.hostname
            if not parsed_url.port and not self.ssl:
                self.port = 80
            elif not parsed_url.port and self.ssl:
                self.port = 443
            elif parsed_url.port:
                self.port = parsed_url.port

            self.base_path = parsed_url.path
            if parsed_url.username:
                self.http_auth = HTTPBasicAuth(
                    username=parsed_url.username, password=parsed_url.password
                )

        if http_auth:
            self.http_auth = http_auth
        self.http_headers = http_headers
        self.group_name = group_name
        self.api_version = api_version
        self.local_download_fallback = local_download_fallback

    @property
    def api_url(self):
        api_url = f"http{'s' if self.ssl else ''}://{self.host}:{self.port}/{self.base_path + '/' if self.base_path else ''}{self.api_version}"
        log.debug(f"api_url: {api_url}")
        return api_url

    def create_request(
        self,
        url: str,
        http_method: Literal["get", "post", "put"] = "get",
        http_query_params: Dict = {},
        http_request_body: Optional[Dict] = {},
        http_header_fields: Dict = {},
        info_description: str = None,
        info_link: str = None,
        hold_request_order: bool = False,
        cache_configuration: RequestCacheConfiguration = None,
    ) -> Request:
        """
        Define a HTTP request to a remote resource.


        **example usage**
        ```python
        import json
        from buffy.buffypyclient import BuffyPyClient
        c = BuffyPyClient() 
        req = c.create_request("https://wikipedia.org")
        ```

        Args:
            url (str): The full URL to the remote resource. Example: "https://mydomain.org/myfile.txt" \
                Optional: Query params can be supplied via a Dict to `http_query_params`
            http_method (Literal["get", "post", "put"], optional): [HTTP Request method](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) for the to be created request
            http_query_params (Dict, optional): [HTTP query string](https://en.wikipedia.org/wiki/Query_string)
            http_request_body (Optional[Dict], optional): [HTTP message body](https://en.wikipedia.org/wiki/HTTP_message_body)
            http_header_fields (Dict, optional): [HTTP header fields](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields)
            info_description (str, optional): This is a documentation string for your request. Buffy server will save your request. \
                For later traceability it can help to give your request some metadata.
            info_link (str, optional): Same as `info_description` but for external metadata
            hold_request_order (bool, optional): The Buffy client will send the request to the buffy server instantly. \
                If for any reasons you need to delay the request, set `hold_request_order` to `True`
            cache_configuration (RequestCacheConfiguration, optional): Buffy server can be configured on when to (re-)download  your request. \
                An instance of `RequestCacheConfiguration` is needed

        Returns:
            BuffyPyClient.Request: An object to handle your request. this is needed to download the content of your request
        """
        api_req = ApiRequest_in(url=url)
        api_req.http_method = http_method
        api_req.http_query_params = http_query_params
        api_req.http_request_body = http_request_body
        api_req.http_header_fields = http_header_fields
        api_req.description = info_description
        api_req.documentation_link = info_link
        api_req.cache_configuration = cache_configuration

        req = BuffyPyClient.Request(api_req, self)
        if hold_request_order:
            return req
        req.order()
        return req
