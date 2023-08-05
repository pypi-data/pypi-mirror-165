import os
import sys

SCRIPT_DIR = "."
if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))

from buffy.buffypyclient import (
    BuffyPyClient,
    ReCachingStrategy,
    RequestCacheConfiguration,
)

remote_file_url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed22n0003.xml.gz"
remote_file_url = "https://www.dundeecity.gov.uk/sites/default/files/publications/civic_renewal_forms.zip"
remote_file_url = "https://filesamples.com/samples/document/txt/sample3.txt"

# connect to buffy server
c = BuffyPyClient(host="localhost", ssl=False)
c.buffy_server_timeout_sec = 1
# create a request

# optional: define a re-caching strategy
cache_config = RequestCacheConfiguration()
cache_config.max_cached_versions = 3
# cache_config.recaching_strategy = ReCachingStrategy.cron(cron="* * * * *")
cache_config.recaching_strategy = ReCachingStrategy.when_requested()


req = c.create_request(url=remote_file_url, cache_configuration=cache_config)

# save requested file
req.download_response_content_to("/tmp/pubmed22n0003.xml.gz")

# or alternatively stream requested file
with open("/tmp/pubmed22n0003_2.xml.gz", "wb") as f:
    for chunk in req.download_response_content():
        f.write(chunk)
