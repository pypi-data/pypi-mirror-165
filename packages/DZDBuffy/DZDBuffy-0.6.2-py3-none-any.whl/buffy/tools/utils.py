from __future__ import annotations
from io import FileIO
import io
from urllib.parse import urlparse
import re
from typing import List, Literal, Type, Union
import hashlib
from pathlib import Path


def extract_domain(url: str):
    parsed = urlparse(url)
    return parsed.hostname


def url_to_path_dir_name(
    url: str,
    object_id: str = None,
    max_length: int = 64,
):
    max_length_minus_id_length = max_length - (len(object_id) + 1 if object_id else 0)
    parsed = urlparse(url)
    base_url_components = f"{parsed.hostname}{'-'+str(parsed.port) if parsed.port and str(parsed.port) not in ['80','443'] else ''}".lower()
    base_url_components += f"{'-'+parsed.path if parsed.path else ''}{'-'+parsed.params if parsed.params else ''}{'-'+parsed.query if parsed.query else ''}".lower()
    cleaned_base = re.sub("[^0-9a-zA-Z]+", "-", base_url_components)
    return f"{cleaned_base[0:max_length_minus_id_length]}{'-'+object_id if object_id else ''}".replace(
        "--", "-"
    )


def is_file_like(obj):
    return (
        isinstance(obj, io.TextIOBase)
        or isinstance(obj, io.BufferedIOBase)
        or isinstance(obj, io.RawIOBase)
        or isinstance(obj, io.IOBase)
        or issubclass(type(obj), io.TextIOBase)
        or issubclass(type(obj), io.BufferedIOBase)
        or issubclass(type(obj), io.RawIOBase)
        or issubclass(type(obj), io.IOBase)
    )


def hashfile(file: Union[str, Path, FileIO], alg: Type[hashlib._Hash] = None) -> str:
    """_summary_

    Args:
        file (Union[str, Path, FileIO]): A path or file like object
        alg (Type[hashlib._Hash], optional): The hashing alg to create the hash of the file. Defaults to hashlib.sha256.

    Returns:
        str: A hex str representing the hash of the file
    """
    # source: https://www.geeksforgeeks.org/compare-two-files-using-hashing-in-python/

    # A arbitrary (but fixed) buffer
    # size (change accordingly)
    # 65536 = 65536 bytes = 64 kilobytes
    if alg == None:
        alg = hashlib.sha256

    BUF_SIZE = 65536

    # Initializing the sha256() method
    hash_: hashlib._Hash = alg()
    seek_pos: int = None
    if is_file_like(file):
        seek_pos = file.tell()
        file.seek(0)
        f = file
    else:
        f = open(file, "rb")
    while True:

        # reading data = BUF_SIZE from
        # the file and saving it in a
        # variable
        data = f.read(BUF_SIZE)

        # True if eof = 1
        if not data:
            break

        # Passing that data to that sh256 hash
        # function (updating the function with
        # that data)
        hash_.update(data)

    if seek_pos:
        # we had an opened file obj. lets restore it to the old state
        file.seek(seek_pos)
    else:
        # we created a local file obj based on a path. lets close it
        f.close()

    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return hash_.hexdigest()


class HttpHeaderContentDispositionParser:
    def __init__(self, content_disposition: str):
        self.raw: str = content_disposition
        self.type: Literal["inline", "attachment", "form-data"] = None
        self.filename_unsafe: str = None
        self.name: str = None
        self._parse()

    def _parse(self):
        if self.raw:
            segments: List[str] = self.raw.split(";")
            if len(segments) in [1, 2, 3]:
                for seg in segments:
                    self._parse_segment(seg)
            else:
                raise ValueError(
                    f"Invalid http header 'content-disposition' syntax. expected sth. as in https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition#syntax got: '{self.raw}'"
                )

    def _parse_segment(self, segment: str):
        segment = segment.strip()
        if segment.lower() in ["inline", "attachment", "form-data"]:
            self.type = segment.lower()
        elif segment.lower().startswith("filename="):
            self.filename_unsafe = (
                segment.split("=")[1].replace('"', "").replace("'", "")
            )
        elif segment.lower().startswith("name="):
            self.name = segment.split("=")[1].replace('"', "").replace("'", "")

    @property
    def filename(self):
        keepcharacters = (" ", ".", "_", "(", ")", "-")
        return "".join(
            c for c in self.filename_unsafe if c.isalnum() or c in keepcharacters
        ).rstrip()
