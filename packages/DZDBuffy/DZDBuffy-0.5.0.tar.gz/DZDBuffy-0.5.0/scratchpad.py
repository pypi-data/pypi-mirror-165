from concurrent.futures import thread
import requests
from email.utils import parsedate_to_datetime


def downloadtest():
    # url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed22n1096.xml.gz"
    # url = "ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed22n1096.xml.gz"
    # url = "http://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/goa_human.gaf.gz"
    url = "https://cloud.connect.dzd-ev.de/s/9fGr79Hwx6D7WZy/download"
    response = requests.head(url)
    print(response.status_code)
    print(response.headers.get("etag", None))
    # print(response.headers["ETag"])
    print(parsedate_to_datetime(response.headers["Date"]))
    print(requests.options(url).headers)
    """
    'Content-Length': '498430'
    'Date': 'Tue, 17 May 2022 12:39:51 GMT'
    'Content-Type': 'image/png'
    'Content-Disposition': 'attachment; filename*=UTF-8\'\'Dashboard.png; filename="Dashboard.png"'
    'Last-Modified': 'Sun, 12 Dec 2021 19:04:35 GMT'
    """


from pathlib import PurePath
from urllib.parse import urlparse


def filenameparser():
    url = "https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse"
    # url = "https://www.youtube.com/?v=QbTb9euNRWg"
    # url = "https://forum.duplicati.com/t/setting-up-amazon-s3/589"
    # url = "https://duplicacy.com/"
    print(PurePath(urlparse(url).path).suffix)


def pure_test():
    p = PurePath("/tmp/file.name")
    print(PurePath(str(p) + ".test"))


def catch_only_non_http_error():
    try:
        raise ValueError("MEH")
        raise requests.exceptions.TooManyRedirects("TOO MANY")
    except requests.exceptions.RequestException as e:
        print("THIS IS A HTTP ERROR")


def catch_thread_error():
    import threading
    import time
    import traceback

    class ThreadWithExpectionStackTraceStatus(threading.Thread):
        def __init__(self, *args, **kwargs):
            self.stack_trace: str = None
            self.failed: bool = False
            super().__init__(**kwargs)

        def run(self):
            try:
                self._target(*self._args, **self._kwargs)
            except:
                self.stack_trace = traceback.format_exc()
                self.failed = True
            finally:
                # Avoid a refcycle if the thread is running a function with
                # an argument that has a member that points to the thread.
                del self._target, self._args, self._kwargs

    def do_stuff():
        time.sleep(1)
        raise ValueError("Meehhooaaauuubooooom")

    t = ThreadWithExpectionStackTraceStatus(target=do_stuff)
    t.start()
    print(t.is_alive())
    print("STUFFF in MAIN")
    time.sleep(2)
    print("STUFFF2 in MAIN")
    try:
        print(t.is_alive())
        t.join()
        print(t.is_alive())
        if t.failed:
            print(t.stack_trace)
    except:
        print("Oh there was an error")


def print_error_msg():
    def make_error():
        raise ValueError("BLABLA")

    try:
        make_error()
    except ValueError as err:
        print(err)


def enumClassTest():
    from enum import Enum

    class TestEnum(str, Enum):
        class Strat:
            def __init__(self, param):
                self.param = param

        VAR = Strat(param=2)

    test = TestEnum.Strat.value

    print(type(test))
    print(test)
    print(test.param)

    # does not work!


def classnametest():
    import inspect

    class BaseWhat:
        def __eq__(self, other):
            if inspect.isclass(other):
                return other.__name__ == self.__class__.__name__
            return isinstance(other, self.__class__)

    class TestWhat(BaseWhat):
        pass

    class TestWhere(BaseWhat):
        pass

    instWhat = TestWhat()
    print(instWhat == TestWhat)
    instWhere = TestWhere()
    print(instWhat == instWhere)
    print(instWhere == TestWhat)
    print(instWhere == TestWhere)


def straStructTest():
    from pydantic import BaseModel
    from typing import Dict, Any, Union
    import inspect
    import json

    class ReCachingStrategy(BaseModel):
        strategy_name: str = None

        def __eq__(self, other):
            if inspect.isclass(other):
                return other.__name__ == self.__class__.__name__
            elif isinstance(other, str):
                return other == self.__class__.__name__
            return isinstance(other, self.__class__)

        def __init__(self, *args, **kwargs):
            super(ReCachingStrategy, self).__init__(*args, **kwargs)
            self.strategy_name = self.__class__.__name__

    class ReCachingStrategies:
        @classmethod
        def from_json(cls, strategy: Union[str, Dict]):
            if isinstance(strategy, str):
                strategy: Dict = json.loads(strategy)
            for strategy_class in cls.list():
                if strategy_class.__name__ == strategy["strategy_name"]:
                    return strategy_class(
                        **{k: v for k, v in strategy.items() if k != "strategy_name"}
                    )

        @classmethod
        def list(cls):
            return [
                cls_attribute
                for cls_attribute in cls.__dict__.values()
                if inspect.isclass(cls_attribute)
            ]

        class never(ReCachingStrategy):
            """never - Strategy
            Once downlaoded we will server only this cached file. no matter how often it is requested.
            This is usefull for files that will be 100% static.
            """

            pass

        class age(ReCachingStrategy):
            """age - Strategy
            Buffy will redownload when the cached version has a certain age in seconds. The default age is 3600sec
            This is usefull for dynamic remote resources, where the webserver wont provide any informations about the state of the resource like "etag", "last_modified_datetime" or "size_in_bytes"

            params:
                seconds - int - default: 3600 - The duration a resource will be cached until it gets a redownload from the source
            """

            seconds: int = 3600

    print(ReCachingStrategies.list())
    st_never = ReCachingStrategies.never()
    st_age = ReCachingStrategies.age()
    st_age_3 = ReCachingStrategies.age(seconds=3)
    print(st_age.json())
    print(st_age_3.json())
    print(st_never.json())
    st_age_3_b = ReCachingStrategies.from_json(st_age_3.json())
    print(st_age_3)
    print(st_age_3.json())


def straStructTest_v2():
    # https://pydantic-docs.helpmanual.io/usage/types/#discriminated-unions-aka-tagged-unions
    from pydantic import BaseModel, Field
    from typing import Dict, Any, Union, Literal
    import inspect

    class ReCachingStrategy(BaseModel):
        strategy_name: str = None

        def __eq__(self, other):
            if inspect.isclass(other):
                return other.__name__ == self.__class__.__name__
            elif isinstance(other, str):
                return other == self.__class__.__name__
            return isinstance(other, self.__class__)

        def __init__(self, *args, **kwargs):
            super(ReCachingStrategy, self).__init__(*args, **kwargs)
            self.strategy_name = self.__class__.__name__

    class ReCachingStrategies:
        @classmethod
        def list(cls):
            return [
                cls_attribute
                for cls_attribute in cls.__dict__.values()
                if inspect.isclass(cls_attribute)
            ]

        class never(ReCachingStrategy):
            """never - Strategy
            Once downlaoded we will server only this cached file. no matter how often it is requested.
            This is usefull for files that will be 100% static.
            """

            # strategy_name: Literal["never"] = "never"

            pass

        class age(ReCachingStrategy):
            """age - Strategy
            Buffy will redownload when the cached version has a certain age in seconds. The default age is 3600sec
            This is usefull for dynamic remote resources, where the webserver wont provide any informations about the state of the resource like "etag", "last_modified_datetime" or "size_in_bytes"

            params:
                seconds - int - default: 3600 - The duration a resource will be cached until it gets a redownload from the source
            """

            # strategy_name: Literal["age"] = "age"
            seconds: int = 3600

    class CachePlan(BaseModel):
        strategy: Union[ReCachingStrategies.never, ReCachingStrategies.age] = Field(
            discriminator="strategy_name"
        )

    print(ReCachingStrategies.list())
    st_never = ReCachingStrategies.never()
    st_age = ReCachingStrategies.age()
    st_age_3 = ReCachingStrategies.age(seconds=3)
    print("COMPARE TO CLASS POS", st_age == ReCachingStrategies.age)
    print("COMPARE TO CLASS NEG", st_age == ReCachingStrategies.never)
    print("CALL CLASS ATTR", ReCachingStrategies.age.seconds)
    print(st_age.json())
    print(st_age_3.json())
    print(st_never.json())
    # st_age_3_b = ReCachingStrategies.from_json(st_age_3.json())
    print(st_age_3)
    print(st_age_3.json())
    plan = CachePlan(strategy=st_age_3)
    print(plan.json())
    plan_parsed = CachePlan.parse_raw(plan.json())
    print(plan_parsed)


def pydantic_args_test():
    from pydantic import BaseModel

    class ReCachingStrategy(BaseModel):

        strategy_name: str = None

    r = ReCachingStrategy(2)
    print(r)
    print(r.json())


def pydantic_dyn_default_test():
    from pydantic import BaseModel, Field

    class naming_bootstrap(BaseModel):
        @classmethod
        def _get_strategy_name(cls) -> str:
            return cls.__name__

    class ReCachingStrategy(naming_bootstrap):

        strategy_name: str = Field(default_factory=naming_bootstrap._get_strategy_name)

        def __init__(self, *args, **kwargs):
            super(ReCachingStrategy, self).__init__(*args, **kwargs)
            # self.strategy_name = Field(self.__class__.__name__, const=True)
            # self.strategy_name = self.__class__.__name__

    r = ReCachingStrategy()
    print(r)  # nope -> strategy_name='naming_bootstrap'


def hashtest():
    import hashlib

    hashlib._Hash
    s = hashlib.sha256()
    print(type(s))


def file_seek_current_pos():
    f = open("README.md")
    f.seek(20)
    print(f.tell())
    f.close()


def is_file_like():
    from tempfile import TemporaryFile
    import io

    io.BufferedRandom

    t = TemporaryFile()
    print(t.tell())
    print(type(t))
    print(issubclass(type(t), io.BufferedIOBase))
    t.close()


def urlparse():
    from urllib.parse import urlparse
    from typing import Callable

    u = urlparse("google.de")
    for attr in dir(u):
        if not attr.startswith("_") and not isinstance(getattr(u, attr), Callable):
            print(attr, getattr(u, attr))


def catch_file_not_exists():
    file = "/tmp/nooooo"
    with open(
        file,
        "rb",
    ) as f:
        while True:
            chunk = f.read(1024)
            if chunk:
                yield chunk
            else:
                break


def redis_url_to_kwargs():
    import redis

    r = redis.Redis.from_url("redis://localhost:6379/0")
    print(r.get_connection_kwargs())


redis_url_to_kwargs()
