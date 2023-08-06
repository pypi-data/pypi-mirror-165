import os
import sys
from fastapi import FastAPI
from typing import Dict, Tuple, Type
from multiprocessing import Process
import logging
from getversion import get_module_version
import time
import click
import redis
import json

log = logging.getLogger(__name__)
if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "../..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))

from Configs import getConfig
from buffy.buffyserver.config import DEFAULT

from buffy.buffyserver.api.v1.api import (
    get_v1_router,
    tags_metadata,
)
from buffy.buffyserver.backend.storage.interface import StorageInterface
from buffy.buffyserver.backend.storage.redis_storage import RedisStorage
from buffy.buffyserver.backend.request_download_service.service import (
    RequestDownloaderService,
)
from pathlib import Path, PurePath

config_file_path = PurePath(Path(__file__).parent.resolve(), "config.py")

logging.basicConfig(
    level=getConfig(config_classes_pathes=[config_file_path]).LOG_LEVEL,
    format="%(asctime)-15s %(processName)-8s %(module)-8s %(levelname)-8s:  %(message)s",
    handlers=[logging.StreamHandler((sys.stdout))],
)
# atm we only have one storage module (redis)
storage_module_mapping: Dict[str, Type[StorageInterface]] = {"redis": RedisStorage}


def _start_api_service():
    import uvicorn

    config: DEFAULT = getConfig(config_classes_pathes=[config_file_path])
    # config: DEFAULT = getConfig()

    app = FastAPI(openapi_tags=tags_metadata)
    storage: StorageInterface = storage_module_mapping[config.STORAGE_BACKEND_MODULE](
        file_storage_dir=config.STORAGE_BACKEND_FILE_DIR,
        config=config.STORAGE_BACKEND_CONFIG,
    )
    app.include_router(get_v1_router(storage), prefix="/v1")

    uvicorn.run(app, **config.UVICORN_PARAMS)


def _start_backend_service():
    # config: DEFAULT = getConfig()
    config: DEFAULT = getConfig(config_classes_pathes=[config_file_path])
    storage: StorageInterface = storage_module_mapping[config.STORAGE_BACKEND_MODULE](
        file_storage_dir=config.STORAGE_BACKEND_FILE_DIR,
        config=config.STORAGE_BACKEND_CONFIG,
    )
    service = RequestDownloaderService(
        storage=storage,
        max_simultaneous_downloads=config.DOWNLOAD_SERVICE_MAX_DOWNLOADS,
        max_simultaneous_downloads_per_domain=config.DOWNLOAD_SERVICE_MAX_DOWNLOADS_PER_DOMAIN,
    )
    service.validate_storage_every_n_sec = config.STORAGE_VALIDATE_EVERY_N_SEC
    service.clean_storage_every_n_sec = config.STORAGE_CLEAN_EVERY_N_SEC
    service.validate_storage_at_boot = config.STORAGE_VALIDATE_ON_BOOT
    service.run()


def start_buffy_server(
    env_vars: Dict = None, watchdog: bool = True
) -> Tuple[Process, Process]:
    if env_vars:
        for k, v in env_vars.items():
            os.environ[k] = json.dumps(v) if isinstance(v, dict) else v

    import buffy
    import pydantic
    import uvicorn

    config: DEFAULT = getConfig(config_classes_pathes=[config_file_path])
    log.info(f"BuffyServer version: '{get_module_version(buffy)[0]}'")
    log.info(f"Pydantic version: '{get_module_version(pydantic)[0]}'")
    log.info(f"Uvicorn version: '{get_module_version(uvicorn)[0]}'")
    log.info(
        f"Storage backend config ('STORAGE_BACKEND_CONFIG'): '{config.STORAGE_BACKEND_CONFIG}'"
    )
    log.info(
        f"Storage backend file dir ('STORAGE_BACKEND_FILE_DIR'): '{config.STORAGE_BACKEND_FILE_DIR}'"
    )
    log.info(f"Uvicorn config ('UVICORN_PARAMS'): '{config.UVICORN_PARAMS}'")
    # toDo: make a more stuborn watchdog process starter.
    backend = Process(target=_start_backend_service, name="Buffy_backend")
    api = Process(target=_start_api_service, name="Buffy_api_service")
    backend.start()
    api.start()
    if watchdog:
        # todo try n-time to rescue/restart a service
        healthy: bool = True
        while healthy:
            if not backend.is_alive():
                backend.join()
                api.terminate()
                api.join()
                raise ValueError(f"Backend exited with code {backend.exitcode}")
            if not api.is_alive():
                api.join()
                backend.terminate()
                backend.join()
                raise ValueError(f"API Service exited with code {api.exitcode}")
            time.sleep(1)
    return backend, api


@click.command(name="buffy-server")
@click.option(
    "--debug/--no-debug",
    help="Enable debug logging",
    default=False,
)
@click.option(
    "--redis-url",
    "-r",
    help="Url to a running Redis database. e.g. 'redis://localhost:6379/0'. For details on the format see https://redis.readthedocs.io/en/latest/connections.html#redis.Redis.from_url",
)
@click.option(
    "--storage-location",
    "-s",
    help="Buffy server will cache http request into this location. e.g. `/var/lib/buffy`",
)
def start_buffy_server_cli(debug: bool, redis_url: str, storage_location: str):
    """Start the buffy server"""
    if debug:
        click.echo(f"Debug mode is on")
        log.setLevel("DEBUG")
        log.debug(f"redis_url({type(redis_url)}):'{redis_url}'")
        log.debug(f"storage_location({type(storage_location)}):'{storage_location}'")
    server_env_vars = {}
    if storage_location:
        Path(storage_location).mkdir(exist_ok=True)
        server_env_vars["CONFIGS_STORAGE_BACKEND_FILE_DIR"] = storage_location
    if redis_url:
        r = redis.Redis.from_url(redis_url)
        server_env_vars["CONFIGS_STORAGE_BACKEND_CONFIG"] = r.get_connection_kwargs()
    start_buffy_server(env_vars=server_env_vars)


@click.command(name="buffy-server-build-api-doc")
@click.option(
    "--target-path",
    "-t",
    help="Url to a running Redis database. e.g. 'redis://localhost:6379/0'. For details on the format see https://redis.readthedocs.io/en/latest/connections.html#redis.Redis.from_url",
)
def build_api_doc(target_path):
    """Generate a the openapi doc"""
    from fastapi.openapi.utils import get_openapi

    app = FastAPI(openapi_tags=tags_metadata)
    app.include_router(get_v1_router(storage=None), prefix="/v1")
    with open(target_path, "w") as f:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
                tags=tags_metadata,
            ),
            f,
        )


if __name__ == "__main__":

    start_buffy_server()
