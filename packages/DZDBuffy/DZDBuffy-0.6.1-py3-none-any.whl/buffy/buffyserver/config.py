from typing import Dict, Literal, Union
from Configs import ConfigBase


class DEFAULT(ConfigBase):
    LOG_LEVEL: str = "INFO"

    #####################
    ### SERVER PARAMS ##
    ###################

    # UVICORN_PARAMS - json/dict - Configuration of the uvicorn webserver which is publishing the Buffy Server API
    # You put any `uvicorn.run` parameter in this dict.
    # See https://www.uvicorn.org/settings/ for all parameters
    UVICORN_PARAMS: Dict = {"port": 8008, "host": "0.0.0.0"}

    #####################
    ### SERVER STORAGE PARAMS ##
    ###################

    STORAGE_BACKEND_MODULE: Literal["redis"] = "redis"

    # STORAGE_BACKEND_CONFIG - json/dict - Configuration for the storage module used.
    # atm only the `redis`-storage-module is supported.
    # The value for key `redis_connection_params` can contain any parameter for the redis python client https://redis.readthedocs.io/en/latest/connections.html#generic-client
    # example:
    # STORAGE_BACKEND_CONFIG = {"file_storage_base_path":"./","redis_connection_params":{"host":"145.23.45.23","port":6379,"password":"s3cret"}}
    STORAGE_BACKEND_CONFIG: Dict = {}

    # STORAGE_BACKEND_FILE_DIR - str: the storage backend can cache files to the local file system. This directory path defines the location for these files
    STORAGE_BACKEND_FILE_DIR: str = "./buffy-server-cache"

    # STORAGE_CLEAN_EVERY_N_SEC - int - How often should be checked if there are old responses that are not needed anymore.
    STORAGE_CLEAN_EVERY_N_SEC: int = 60

    # STORAGE_VALIDATE_EVERY_N_SEC - int - When validating every cached response is checked for unexpexted changes. If any occure buffy will delete these responses.
    # This can happen on unrealiable storage or when the storage is whipped by external processes (e.g. container restart without volumes)
    STORAGE_VALIDATE_EVERY_N_SEC: int = 43200

    # STORAGE_VALIDATE_ON_BOOT - bool - see STORAGE_VALIDATE_EVERY_N_SEC but should be one run started when buffy server is starting?
    STORAGE_VALIDATE_ON_BOOT: bool = True

    # DOWNLOAD_SERVICE_MAX_DOWNLOADS - int - How many downloads simultaniously should be started in the background?
    DOWNLOAD_SERVICE_MAX_DOWNLOADS: int = 4
    # DOWNLOAD_SERVICE_MAX_DOWNLOADS_PER_DOMAIN - int - How many downloads simultaniously should be started in the background per domain?
    DOWNLOAD_SERVICE_MAX_DOWNLOADS_PER_DOMAIN: int = 1
