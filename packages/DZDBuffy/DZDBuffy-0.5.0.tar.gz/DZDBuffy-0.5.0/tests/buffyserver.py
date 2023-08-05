from distutils.command.config import config
import os
import sys
import time
import subprocess
from shittywebserver import run_shitty_webserver
import requests
from pathlib import Path
import json

print("# Create server instances...")
SCRIPT_DIR = "."
if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))
STORAGE_BASE_DIR = "./tests/tmp"
STORAGE_CLIENT = f"{STORAGE_BASE_DIR}/client"
STORAGE_SERVER = f"{STORAGE_BASE_DIR}/server"
os.makedirs(STORAGE_CLIENT, exist_ok=True)
os.makedirs(STORAGE_SERVER, exist_ok=True)
os.environ["CONFIGS_STORAGE_BACKEND_CONFIG"] = json.dumps(
    {
        "file_storage_base_path": STORAGE_SERVER,
        "redis_connection_params": {},
    }
)
from buffy.buffyserver.api.v1.models import Request_in, Request, Response
from buffy.buffyserver.main import start_buffy_server
from buffy.buffypyclient import (
    BuffyPyClient,
    RequestCacheConfiguration,
    ReCachingStrategy,
)


BUFFY_BASE_URL = "http://localhost:8008/v1/"
SHITTY_WEBSERVER_BASE_URL = "http://localhost:8088/v1/"


print("Start shittywebserber as test endpoint...")
webserver_proc = run_shitty_webserver(port=8088, run_in_subprocess=True)
time.sleep(1)
print("Start Buffy instance...")
backend_proc, api_proc = start_buffy_server()
time.sleep(1)


def do_request(endpoint: str):
    url = SHITTY_WEBSERVER_BASE_URL + endpoint
    # url = "https://releases.ubuntu.com/22.04/ubuntu-22.04-desktop-amd64.iso"
    r = Request_in(url=url)
    print("RUN:", endpoint, r.json())
    res: requests.Response = requests.put(BUFFY_BASE_URL + "request/", data=r.json())
    res.raise_for_status()
    buffy_req: Request = Request.parse_raw(res.content)
    response_done: bool = False
    time.sleep(60)
    while not response_done:
        rsp_wait = requests.get(
            BUFFY_BASE_URL + f"request/{buffy_req.id}/response/latest", data=r.json()
        )
        if rsp_wait.content == b"null":
            time.sleep(0.5)
            continue
        buffy_res: Response = Response.parse_raw(rsp_wait.content)
        if buffy_res.status in ["wait", "in_progress"]:
            time.sleep(0.5)
            continue
        if buffy_res.status == "ready":
            response_done = True
    print("content_download_url", buffy_res.content_download_path)


# do_request("download/static-content-static-etag?size_bytes=104857600")
# do_request("download/slow?size_bytes=5048500&chunk_wait_time=0.002")
do_request("download/do-nothing")

## clean up

import atexit


def shut_down():
    print("Shut down test env...")
    backend_proc.terminate()
    api_proc.terminate()
    webserver_proc.terminate()


atexit.register(shut_down)
