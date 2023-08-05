# Wikidata.org - Only update data every quarter

___

Lets query all countries with their goverment form from wikidata.org. 
The wikidata.org API can be - understandably - a little bit sensitive when beating their servers. 
The queries can be quite expensive. Thats why it wont take too much to get a `429 Too Many Requests`.  
Lets use Buffy to dampen our wikidata server usage.  
As Countries are relatively static concepts we are happy in this scenario, if we only update the request data every quarter.


```python
import json
from buffy.buffypyclient import BuffyPyClient,ReCachingStrategy,RequestCacheConfiguration

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

# define a strategy on server background recaching. 
# This will relieve the wikidata.org server, no matter how often we request the data.
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
```

The cool thing with `ReCachingStrategy.age` that reCaching will happen in the background.   
So next quarter, when running our code again, the data will allready be available. We dont have to wait for the wikidata.org server to process our query.


# Pinning a certain version

todo