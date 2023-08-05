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