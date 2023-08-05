import os
import sys

SCRIPT_DIR = "."
if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))


from buffy.buffypyclient import BuffyPyClient

c = BuffyPyClient()
req = c.create_request(url="https://www.foaas.com/awesome/:tim")
cached_responses = req.list_cached_response_versions()
for resp in cached_responses:
    print(resp.id)
