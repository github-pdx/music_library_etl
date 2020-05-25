# *Music Library* ETL

[![Build Status](https://travis-ci.com/github-pdx/media_etl.svg?branch=master)](https://travis-ci.com/github-pdx/media_etl)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Python v3.7 script to ETL media tags:
Extract '.mp3', '.mp4', '.flac', and '.wma' tag data from JSON to Postgres

*Extract:* read from JSON flat file (database)
*Transform:* convert from JSON dictionary format to SQL
*Load:* write data to destination database (Postgres)

## Examples
![Screenshot](https://github.com/github-pdx/media_etl/blob/master/img/json_input.png)

![Screenshot](https://github.com/github-pdx/media_etl/blob/master/img/postgres_media_db.png)

* [JSON](https://github.com/github-pdx/media_etl/blob/master/data/input/media_lib.json)

## Tested On:
* Ubuntu 16.04 LTS (Xenial Xerus)
* Ubuntu 18.04 LTS (Bionic Beaver)
* CentOS 8 (RHEL)
* Windows 10 version 1909


## Optional:
* [Install Docker](https://www.docker.com/products/docker-desktop)

* [Docker Commands](https://docs.docker.com/engine/reference/commandline/build/)
```
# start Postgres in Docker
docker-compose up --build
docker ps
docker-compose ps
docker exec -it {CONTAINER_ID} /bin/bash
docker-compose run media_etl sh -c "python ./media_etl/postgres_etl.py -p=5432"
# once Docker is up, run scripts from PyCharm IDE on host
python ./media_etl/postgres_etl.py -p=5432
# hit CTRL-C to exit Postgres in Docker
docker-compose down --remove-orphans
```

* [Install Postgres](https://www.postgresql.org/download/)

* [Postgres Shell Commands](https://www.postgresql.org/docs/12/app-psql.html)
```
sudo sed -i 's/port = 5432/port = 5433/g' /etc/postgresql/12/main/postgresql.conf
sudo service postgresql restart
sudo lsof -iTCP -sTCP:LISTEN | grep postgres
systemctl status postgres
psql -c "CREATE DATABASE media_db;" -U postgres
psql -c "CREATE USER run_admin_run WITH PASSWORD 'run_pass_run';" -U postgres
```

* [Spotify Authorization](https://developer.spotify.com/documentation/general/guides/authorization-guide/)
```
[spotify.com]
SPOTIPY_CLIENT_ID = 123456789abcdefg        <-- enter your CLIENT_ID here
SPOTIPY_CLIENT_SECRET = abcdefg123456789    <-- enter your CLIENT_SECRET here
```

## License:
[MIT License](LICENSE)
