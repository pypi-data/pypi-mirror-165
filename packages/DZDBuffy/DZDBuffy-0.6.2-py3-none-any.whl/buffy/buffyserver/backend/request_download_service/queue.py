from typing import List, Dict, Tuple, Literal, Set
import threading
from io import FileIO
import traceback
from buffy.buffyserver.api.v1.models import Request, Response, Request_in
from buffy.tools.stuborn_downloader import StubornDownloader
from buffy.tools.utils import extract_domain


class Download:
    class ThreadWithExpectionStackTraceStatus(threading.Thread):
        def __init__(self, *args, **kwargs):
            self.error_stack_trace: str = None
            self.error: Exception = None
            self.failed: bool = False
            super().__init__(**kwargs)

        def run(self):
            try:
                self._target(*self._args, **self._kwargs)
            except Exception as err:
                self.error = err
                self.error_stack_trace = traceback.format_exc()
                self.failed = True
            finally:
                # Avoid a refcycle if the thread is running a function with
                # an argument that has a member that points to the thread.
                del self._target, self._args, self._kwargs

    def __init__(self, request: Request, response: Response, file_target: FileIO):
        self.request = request
        self.response = response
        self.domain = extract_domain(request.url)
        self.downloader = StubornDownloader(request=request)
        self.thread = Download.ThreadWithExpectionStackTraceStatus(
            target=self.downloader.download,
            args=(
                None,
                file_target,
            ),
        )

    @property
    def status(self) -> Literal["wait", "run", "finished"]:
        if self.thread.ident is None:
            return "wait"
        elif self.thread.is_alive():
            return "run"
        else:
            return "finished"


class RequestDownloadQueue:
    def __init__(self):
        self.downloads: List[Download] = []

    def get_downloads(
        self,
        by_domain: str = None,
        by_status: Literal["wait", "run", "finished"] = None,
    ) -> List[Download]:
        return [
            d
            for d in self.downloads
            if (d.domain == by_domain or by_domain is None)
            and (d.status == by_status or by_status is None)
        ]

    @property
    def domains(self) -> Set:
        return set([d.domain for d in self.downloads])

    def add_download(self, request: Request, response: Response, file_target: FileIO):
        self.downloads.append(
            Download(request=request, response=response, file_target=file_target)
        )

    def remove_download(self, download: Download):
        self.downloads.remove(download)
