import os
import sys
from pathlib import Path, PurePath

SCRIPT_DIR = None
if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))

from buffy.tools.stuborn_downloader import (
    StubornDownloader,
    BuffyRequest,
    ResponseDownloadStats,
)

file = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed22n0003.xml.gz"
file = "https://releases.ubuntu.com/22.04/ubuntu-22.04-desktop-amd64.iso"
file = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/100.0.1/linux-x86_64/de/firefox-100.0.1.tar.bz2"
file = "https://filesamples.com/samples/document/txt/sample3.txt"

print_status = True


def hook_status_updates(status: ResponseDownloadStats):
    if print_status:
        print("STATUS FROM HOOK", status)


def test_target_path():
    trgt = PurePath(SCRIPT_DIR, "tests", "tmp")
    req = BuffyRequest(url=file)
    d = StubornDownloader(request=req)
    # print("STATUS FROM CALLER", d.status)
    d.hook_status_updates = hook_status_updates
    # print(d.get_response_content_attrs(cached_only=False))
    d.download(target_dir=trgt)
    print(d.response_header_fields)
    # print("STATUS FROM CALLER", d.status)
    # print(d.byte_position)
    # print(d.get_response_content_attrs(cached_only=False))


def test_file_obj():
    trgt_dir = PurePath(
        SCRIPT_DIR,
        "tests",
        "tmp",
    )
    trgt_file = PurePath(trgt_dir, "myfile.part")
    file_obj = open(trgt_file, "ab")
    req = BuffyRequest(url=file)
    d = StubornDownloader(request=req)

    d.hook_status_updates = hook_status_updates

    d.download(file_obj=file_obj)
    os.rename(trgt_file, PurePath(trgt_dir, d.get_response_content_attrs().filename))


test_target_path()
