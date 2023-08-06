There are multiple options to start your own Buffy server:

## Via Docker-compose

___

### Requirements

* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/compose-plugin/)

### Server start

* Download the buffy docker-compose file 

```bash
wget -O docker-compose.yaml https://git.connect.dzd-ev.de/dzdpythonmodules/buffy/-/raw/main/docker-compose.yaml?inline=false
```

* Start the Buffy server with docker compose

```bash
docker-compose up -d
```

### Usage

Now your Buffy server is available at `http://localhost:8008`


## Via Docker image

___

### Requirements

* [Docker](https://docs.docker.com/engine/install/)
* A running [Redis](https://redis.io/) Instance

### Start the official image

```bash
docker run -p 8008:8008 -v ${PWD}/buffy-server-cache:/data registry-gl.connect.dzd-ev.de:443/dzdpythonmodules/buffy:prod -r redis://my-redis-server
```

For details on the possible parameters see [`Via Terminal`](#buffy-server-command-parameters)

### Start your local build image

```bash
git clone ssh://git@git.connect.dzd-ev.de:22022/dzdpythonmodules/buffy.git
```

```bash
cd buffy
```

```bash
docker build . -t buffy
```

```bash
docker run -p 8008:8008 -v ${PWD}/buffy-server-cache:/data buffy -r redis://my-redis-server
```

## Via Terminal

___

### Requirements

* Python >= 3.8
* A running [Redis](https://redis.io/) Instance


### Start the official pip package

```bash
pip install DZDBuffy
```

```bash
buffy-server
```

### Start a local clone of the source

```bash
git clone ssh://git@git.connect.dzd-ev.de:22022/dzdpythonmodules/buffy.git
```
```bash
cd buffy
```

**Optional:** jump to latest stable release state
```
# Get new tags from remote
git fetch --tags
# Get latest tag name
latestTag=$(git describe --tags `git rev-list --tags --max-count=1`)
# Checkout latest tag
git checkout $latestTag
```


Install buffy and 3rd party python modules
```bash
pip install --no-cache-dir -e .
```

```bash
buffy-server
```

### `buffy-server` Command Parameters

___

#### `--debug`

Changes python logging from `INFO` to `DEBUG`

example:  
```
buffy-server --debug
```

___

#### `--redis-url`

Url to a running Redis database. e.g. 'redis://localhost:6379/0'.  
For details on the format see https://redis.readthedocs.io/en/latest/connections.html#redis.Redis.from_url

short form: `-r`

example:
```
buffy-server --redis-url redis://localhost:6379/0
```
```
buffy-server --r rediss://redis-server.mydomain.org:6379/0
```

___


#### `--storage-location`

Local storage location for cached requests

short form: `-s`

examples:
```bash
buffy-server --storage-location /var/lib/buffy
```

```bash
buffy-server --s /opt/buffy
```


## Authentication

At the moment Buffy does not support native Authentication. But you can easily put a nginx reverse proxy in front of Buffy to restrict access to Buffy.

For convenience we use a pre-configured nginx image https://hub.docker.com/r/beevelop/nginx-basic-auth / https://github.com/beevelop/docker-nginx-basic-auth

For a production environment you may want to build your own nginx setup.

On Linux install apache2-utils and **create a http digest basic authentication string**:

```bash
sudo apt install apache2-utils
```

You want to replace `$`with double `$$` to escape them in docker-compose. a `| sed "s/\\$/\$\$/g"` will do this for us: 

```bash
echo "mySuperPasswort" | htpasswd -i -n MyUsername | sed "s/\\$/\$\$/g"
```

Lets put it all together in a docker compose file

```yaml
version: "3.7"

services:
  redis:
    image: redis:alpine
    container_name: buffy_redis
    command: redis-server --save 12 1 --loglevel warning
    volumes:
      - ${PWD}/buffy-server-cache/redis:/data
  buffy-server:
    image: registry-gl.connect.dzd-ev.de:443/dzdpythonmodules/buffy:prod
    container_name: buffy_server
    volumes:
      - ${PWD}/buffy-server-cache/buffy-server:/data
  auth:
    image: beevelop/nginx-basic-auth
    container_name: buffy_auth
    ports:
      - 8008:80
    environment:
      FORWARD_PORT: 8008
      FORWARD_HOST: buffy_server
      HTPASSWD: "MyUsername:$$apr1$$oAPV7ijv$$RapWngyr74pRsF0nZY/6o1"
```

### Authentication in the BuffyPyClient

To use our new authenticating server, we just need to supply our credentials via a `requests.auth.HTTPBasicAuth` instance

```python
from buffy.buffypyclient import BuffyPyClient
from requests.auth import HTTPBasicAuth

# connect to buffy server with the credentials
c = BuffyPyClient(
    host="localhost",
    port=8008,
    ssl=False,
    local_download_fallback=False,
    http_auth=HTTPBasicAuth(username="MyUsername", password="mySuperPasswort"),
)

# create a request as usual
req = c.create_request(
    url="http://purl.obolibrary.org/obo/bfo.owl",
)
# save requested file
owl_file = ""
for chunk in req.download_response_content():
    owl_file += chunk.decode("utf-8")
print(owl_file)
```