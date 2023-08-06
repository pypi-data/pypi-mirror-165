import os

import sys
import time
import pydantic
from shittywebserver import run_shitty_webserver
import json
import atexit
import shutil
from pathlib import Path
import multiprocessing
from typing import List
import requests

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
CLEAN_RESULT_FILES_AT_EXIT: bool = True
BUFFY_SERVER_URL = "http://localhost:8008"
os.makedirs(STORAGE_CLIENT, exist_ok=True)
os.makedirs(STORAGE_SERVER, exist_ok=True)
STORAGE_CLEAN_INTERVAL_SEC = 10

SHITTY_WEBSERVER_BASE_URL = "http://localhost:8088/v1"

REDIS_HOST = os.getenv("CI_REDIS_HOST", "localhost")
print("REDIS_HOST", REDIS_HOST)
STORAGE_CONF = {"host": REDIS_HOST}
LOG_LEVEL = "DEBUG"


def end(exit=False):
    webserver_proc.kill()
    api_proc.kill()
    backend_proc.kill()
    if CLEAN_RESULT_FILES_AT_EXIT and os.path.isdir(STORAGE_BASE_DIR):
        print(f"CLEAR '{STORAGE_BASE_DIR}'")
        shutil.rmtree(STORAGE_BASE_DIR)
    if exit:
        exit()


atexit.register(end)

from buffy.buffyserver.api.v1.models import Request_in, Request, Response
from buffy.buffyserver.main import start_buffy_server
from buffy.buffypyclient import (
    BuffyPyClient,
    RequestCacheConfiguration,
    ReCachingStrategy,
)
from buffy.tools.utils import hashfile


print("Start shittywebserber as test endpoint...")
webserver_proc = run_shitty_webserver(port=8088, run_in_subprocess=True)
time.sleep(1)
print("Start Buffy instance...")

backend_proc, api_proc = start_buffy_server(
    env_vars={
        "CONFIGS_STORAGE_BACKEND_CONFIG": json.dumps(STORAGE_CONF),
        "CONFIGS_STORAGE_BACKEND_FILE_DIR": STORAGE_SERVER,
        "CONFIGS_STORAGE_CLEAN_EVERY_N_SEC": STORAGE_CLEAN_INTERVAL_SEC,
        "CONFIGS_LOG_LEVEL": LOG_LEVEL,
    },
    watchdog=False,
)
time.sleep(1)


def run_test_func(func, timeout_sec=60):
    print(f"## RUN TEST '{func.__name__}' with timeout of {timeout_sec} secs ")

    def check_backend_health():
        if not backend_proc.is_alive():
            backend_proc.join()
            return Exception(f"Backend error exitcode: {backend_proc.exitcode}")
        if not api_proc.is_alive():
            api_proc.join()
            return Exception(f"API Server error exitcode: {api_proc.exitcode}")

    start_time = time.time()
    p = multiprocessing.Process(target=func)
    p.start()
    while p.is_alive():
        server_exc = check_backend_health()
        if server_exc:
            p.terminate()
            p.join()
            raise server_exc
        if time.time() - start_time > timeout_sec:
            p.terminate()
            p.join()
            raise TimeoutError()
        time.sleep(0.1)
    p.join()
    if p.exitcode > 0:
        raise ValueError(f"## TEST '{func.__name__}' failed. Exitcode: {p.exitcode}")

    return


try:
    print("# Run tests...")
    bclient = BuffyPyClient(BUFFY_SERVER_URL)

    def test_client_params():
        c = BuffyPyClient(host="localhost", ssl=False)
        assert c.api_url == f"{BUFFY_SERVER_URL}/v1"
        c = BuffyPyClient(ssl=True)
        assert c.api_url == "https://localhost:8008/v1"
        c = BuffyPyClient(url="https://example.de")
        assert c.api_url == "https://example.de:443/v1"

    def ten_meg_static():
        print("## Ten megs static...")
        files = []
        for i in [0, 3]:
            time.sleep(i)
            req_one_mb_cron = bclient.create_request(
                f"{SHITTY_WEBSERVER_BASE_URL}/download/static-content-static-etag?size_bytes=10485760",
                cache_configuration=RequestCacheConfiguration(
                    recaching_strategy=ReCachingStrategy.never()
                ),
                info_description="ten_meg_static",
            )
            path = f"{STORAGE_CLIENT}/ten_mb_static_never{i}.file"
            req_one_mb_cron.download_response_content_to(path)
            files.append(path)
        # we should recieve 2 times the same cached file
        assert hashfile(files[0]) == hashfile(files[1])

    def ten_meg_din_cron():
        print("## one meg dynamic, CRON strat...")
        url = f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=1048576"
        first_file = bclient.create_request(
            url,
            cache_configuration=RequestCacheConfiguration(
                recaching_strategy=ReCachingStrategy.cron(
                    cron="* * * * * */10",
                    run_at_start=False,  # recache every 10 seconds
                )
            ),
            info_description="ten_meg_din_cron",
        )
        first_path = first_file.download_response_content_to(
            f"{STORAGE_CLIENT}/one_dyn_cron_mb_1.file"
        )
        time.sleep(10)
        second_file = bclient.create_request(url, hold_request_order=True)
        second_file.order(prefer_cached=False)
        second_path = second_file.download_response_content_to(
            f"{STORAGE_CLIENT}/one_dyn_cron_mb_2.file"
        )
        # the files should differ as it was recached
        assert hashfile(first_path) != hashfile(second_path)

        # disable recaching as test has ended
        first_file.cache_configuration = RequestCacheConfiguration(
            recaching_strategy=ReCachingStrategy.never()
        )

    def ten_meg_din_age():
        print("## one meg dynamic, AGE strat...")
        files = []
        for i in [0, 1, 16]:
            time.sleep(i)
            req_one_mb_age = bclient.create_request(
                f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=1048575",
                info_description="ten_meg_din_age",
                hold_request_order=True,
            )
            req_one_mb_age.cache_configuration = RequestCacheConfiguration(
                max_cached_unpinned_versions=3,
                recaching_strategy=ReCachingStrategy.age(
                    seconds=6
                ),  # recache every 6 seconds
            )
            req_one_mb_age.order(prefer_cached=False)
            path = f"{STORAGE_CLIENT}/one_dyn_age_mb{i}.file"
            req_one_mb_age.download_response_content_to(path)
            files.append(path)

        # the first 2 files were downloaded before the file 'aged'. they should be the same:
        assert hashfile(files[0]) == hashfile(files[1])
        # the third file was recached by the buffy server after 10 seconds because if its age.
        # it should be a different file
        assert hashfile(files[0]) != hashfile(files[2])
        # Disable recaching as test is completed
        req_one_mb_age.cache_configuration = RequestCacheConfiguration(
            recaching_strategy=ReCachingStrategy.never()
        )

    def filename_test():

        req_one_mb_age = bclient.create_request(
            f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=1048575",
            info_description="filename_test",
        )

        req_one_mb_age.cache_configuration = RequestCacheConfiguration(
            recaching_strategy=ReCachingStrategy.never()
        )

        target_path = req_one_mb_age.download_response_content_to(dir=STORAGE_CLIENT)

        assumed_target_path = Path(f"{STORAGE_CLIENT}/rand_bytes.bytes")
        print(target_path, assumed_target_path)
        assert target_path == assumed_target_path

    def test_download_to_dir():

        size = 1048575
        r = bclient.create_request(
            f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes={size}",
            info_description="test_download_to_dir",
        )
        p = r.download_response_content_to(dir=STORAGE_CLIENT)
        assert p.stat().st_size == size

    def test_local_download_to_dir():
        c = BuffyPyClient(host="non-existing-host", ssl=False)
        size = 1048576
        r = c.create_request(
            f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes={size}"
        )
        p = r.download_response_content_to(dir=STORAGE_CLIENT)
        assert p.stat().st_size == size

    def multiple_requests_with_when_req():
        def start_one_req(index):
            c = BuffyPyClient(url=BUFFY_SERVER_URL, local_download_fallback=False)
            size = 1048573
            r = c.create_request(
                f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes={size}",
                cache_configuration=RequestCacheConfiguration(
                    recaching_strategy=ReCachingStrategy.when_requested()
                ),
            )
            p = r.download_response_content_to(f"{STORAGE_CLIENT}/MP_WR_{index}")
            assert p.stat().st_size == size

        req_count = 5
        req_procs: List[multiprocessing.Process] = []
        timeout = 10
        start_time = time.time()
        for i in range(0, req_count):
            req_procs.append(multiprocessing.Process(target=start_one_req, args=(i,)))

        for proc in req_procs:
            proc.start()

        while all([p.is_alive() for p in req_procs]):
            if time.time() - start_time > timeout:
                for proc in req_procs:
                    proc.terminate()
                    raise TimeoutError()
        for proc in req_procs:
            proc.join()
        hashes = []
        for i in range(0, req_count):
            hashes.append(hashfile(f"{STORAGE_CLIENT}/MP_WR_{i}"))
        # TODO: find a way to assert results...
        print(hashes)

    def keep_certain_version_find_by_tag():
        url = f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=10485"

        req_keep = bclient.create_request(
            url,
            cache_configuration=RequestCacheConfiguration(
                recaching_strategy=ReCachingStrategy.when_requested(),
                max_cached_unpinned_versions=1,
            ),
            info_description="keep_certain_version_find_by_tag",
        )
        req_keep.download_response_content_to(f"{STORAGE_CLIENT}/keep.file")
        keep_version = req_keep.response_version
        req_keep.pin()
        req_keep.tag("keep-it")
        time.sleep(1)
        req_new = bclient.create_request(url, hold_request_order=False)
        req_new.order(prefer_cached=False)
        req_new.download_response_content_to(f"{STORAGE_CLIENT}/keep_not.file")
        keep_not_version = req_new.response_version
        assert (
            keep_version != keep_not_version
        ), f"{keep_version},{keep_not_version} are the same"
        time.sleep(1)
        req_keep_redownload = bclient.create_request(url, hold_request_order=False)
        req_keep_redownload.order(force_tag="keep-it")
        req_keep_redownload.download_response_content_to(
            f"{STORAGE_CLIENT}/keep_redownload.file"
        )
        keep_redownload_version = req_keep_redownload.response_version
        assert (
            keep_redownload_version == keep_version
        ), f"{keep_redownload_version},{keep_version} are not the same"

    def duplicate_test():
        url = f"{SHITTY_WEBSERVER_BASE_URL}/download/static-content-static-etag?size_bytes=32"

        for i in range(0, 3):
            req = bclient.create_request(
                url,
                cache_configuration=RequestCacheConfiguration(
                    recaching_strategy=ReCachingStrategy.when_requested(),
                    max_cached_unpinned_versions=1,
                ),
                info_description="generate duplicates",
            )
            time.sleep(1)
        time.sleep(3)
        versions = req.list_cached_response_versions(status=None)
        dups = [r for r in versions if r.status == "duplicate"]
        ready = [r for r in versions if r.status == "ready"]
        assert len(ready) == 1, f"we have {len(ready)} ready respones exptected 1"
        assert (
            len(dups) > 1
        ), f"we have {len(dups)} duplicate respones expected more than one 1"

    def pin_first():
        url = f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=32"

        for i in range(0, 3):
            req = bclient.create_request(
                url,
                cache_configuration=RequestCacheConfiguration(
                    recaching_strategy=ReCachingStrategy.when_requested(),
                    max_cached_unpinned_versions=1,
                    max_cached_pinned_versions=1,
                ),
                info_description="pin_first",
            )
            if i == 0:
                req._wait_for_response_completion()
                pinned_version = req.pin()
            time.sleep(1)
        time.sleep(STORAGE_CLEAN_INTERVAL_SEC)
        versions = req.list_cached_response_versions(status=None)
        pinned_versions = [v for v in versions if v.is_pinned]
        unpinned_versions = [v for v in versions if not v.is_pinned]
        assert (
            len(versions) == 2
        ), f"Cleaning not happened. to many versions. expected 2 versions got {len(versions)}"
        assert (
            pinned_versions[0].version == pinned_version
        ), f"Pinned version {pinned_version} is not listed pinned_versions: {pinned_versions}"

    def tag_first():
        url = f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=64"

        for i in range(0, 3):
            req = bclient.create_request(
                url,
                cache_configuration=RequestCacheConfiguration(
                    recaching_strategy=ReCachingStrategy.when_requested(),
                    max_cached_unpinned_versions=4,
                    max_cached_pinned_versions=1,
                ),
                info_description="tag_first",
            )
            if i == 0:
                req._wait_for_response_completion()
                tagged_version_name = req.tag("MY-TAG-BEST-TAG")
            time.sleep(1)
        time.sleep(STORAGE_CLEAN_INTERVAL_SEC)
        tagged_versions = req.list_cached_response_versions(
            status=None, tag="MY-TAG-BEST-TAG"
        )

        assert (
            len(tagged_versions) == 1
        ), f"Expected 1 tagged version got {len(tagged_versions)}"
        assert tagged_versions[0].version == tagged_version_name

    def wrong_tag():
        url = f"{SHITTY_WEBSERVER_BASE_URL}/download/random-content-static-etag?size_bytes=43"

        req = bclient.create_request(
            url,
            info_description="wrong_tag",
        )

        req._wait_for_response_completion()
        #######################
        catched_bad_name = False
        try:
            tagged_version_name = req.tag(
                "EVIL-TAG-TOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO-LOOOOOOOOOOONG"
            )
        except pydantic.error_wrappers.ValidationError as e:
            print(e)
            catched_bad_name = True
        assert catched_bad_name
        #######################
        catched_bad_name = False
        try:
            tagged_version_name = req.tag("EVIL TAG BAD CHARS %&/§")
        except pydantic.error_wrappers.ValidationError as e:
            print(e)
            catched_bad_name = True
        assert catched_bad_name

    def timed_out_download():
        # todo
        pass

    def failed_download():
        # todo
        pass

    run_test_func(wrong_tag, 5)
    run_test_func(tag_first, STORAGE_CLEAN_INTERVAL_SEC + 10)
    run_test_func(pin_first, STORAGE_CLEAN_INTERVAL_SEC + 10)
    run_test_func(test_client_params, 5)
    run_test_func(test_client_params, 5)
    run_test_func(ten_meg_static, 60)
    run_test_func(ten_meg_din_cron, 60)
    run_test_func(ten_meg_din_age, 60)
    run_test_func(filename_test, 10)
    run_test_func(test_download_to_dir, 20)
    run_test_func(test_local_download_to_dir, 20)
    run_test_func(multiple_requests_with_when_req, 20)
    run_test_func(keep_certain_version_find_by_tag, 20)
    run_test_func(duplicate_test, 20)


except:
    end(exit=False)
    raise
end()
