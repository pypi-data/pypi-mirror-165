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

import json

# connect to buffy server
from buffy.buffypyclient import (
    BuffyPyClient,
    ReCachingStrategy,
    RequestCacheConfiguration,
)

# connect to buffy server
c = BuffyPyClient(host="localhost", port=8008, ssl=False)

wikidata_query = """
SELECT DISTINCT ?Country ?CountryLabel ?gov_form ?gov_formLabel WHERE {
    ?Country p:P31/ps:P31 wd:Q6256;
        wdt:P37 ?official_language ;
        wdt:P297 ?ISO_3166_1_alpha_2_code ;
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    OPTIONAL { ?Country wdt:P47 ?sharesBorderWith. }
    OPTIONAL { ?Country wdt:P122 ?gov_form. }
    } ORDER BY ?CountryLabel
"""

# define a strategy on server background  recaching. Countries are relatively static concepts.
# In this example we are happy, if we update the request data every quarter.
# This will relieve the wikidata.org server, no matter how often we request the data.
# Also we wont get on any blacklist if we request to often.
strategy = ReCachingStrategy.age(seconds=60 * 60 * 24 * 92)
# Lets pack the strategy in our Cache config
config = RequestCacheConfiguration(recaching_strategy=strategy, max_cached_versions=3)

# create a request
req = c.create_request(
    url="https://query.wikidata.org/sparql",
    http_query_params={"format": "json", "query": wikidata_query},
    http_header_fields={
        "user-agent": "MyTestClient",
        "Accept": "application/json",
    },
    cache_configuration=config,
)
# save requested file
countries = ""
for chunk in req.download_response_content():
    countries += chunk.decode("utf-8")
print(json.loads(countries))
