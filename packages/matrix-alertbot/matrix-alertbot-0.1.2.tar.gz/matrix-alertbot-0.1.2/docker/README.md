# Docker

The docker image will run matrix-alertbot with a SQLite database and
end-to-end encryption dependencies included. For larger deployments, a
connection to a Postgres database backend is recommended.

## Setup

### The `/data` volume

The docker container expects the `config.yaml` file to exist at
`/data/config.yaml` . To easily configure this, it is recommended to create a
directory on your filesystem, and mount it as `/data` inside the container:

```
mkdir data
```

We'll later mount this directory into the container so that its contents
persist across container restarts.

### Creating a config file

Copy `config.sample.yaml` to a file named `config.yaml` inside of your newly
created `data` directory. Fill it out as you normally would, with a few minor
differences:

* The bot store directory should reside inside of the data directory so that it
  is not wiped on container restart. Change it from the default to
`/data/store` . There is no need to create this directory yourself, it will be
  created on startup if it does not exist.

* The bot cache directory should reside inside of the data directory as well, 
  so that alerts and silences related informations are not wiped on container 
  restart. Change it from the default to `/data/cache` .
  There is no need to create this directory yourself, it will be created on 
  startup if it does not exist.

Change any other config values as necessary. For instance, you may also want to
store log files in the `/data` directory.

## Running

First, create a volume for the data directory created in the above section:

```
docker volume create \
  --opt type=none \
  --opt o=bind \
  --opt device="/path/to/data/dir" matrix-alertbot
```

Start the bot with:

```
docker-compose up --build
```

This will run the bot and log the output to the terminal. You can instead run
the container detached with the `-d` flag:

```
docker-compose up -d --build
```

(Logs can later be accessed with the `docker-compose logs` command).

This will build an optimized, production-ready container.

## Systemd

A systemd service file is provided for your convenience at
[matrix-alertbot.service](matrix-alertbot.service). The service uses
`docker-compose` to start and stop the bot.

Copy the file to `/etc/systemd/system/matrix-alertbot.service` and edit to
match your setup. You can then start the bot with:

```
systemctl start matrix-alertbot
```

and stop it with:

```
systemctl stop matrix-alertbot
```

To run the bot on system startup:

```
systemctl enable matrix-alertbot
```

## Building the image

To build a production image from source, use the following `docker build` command
from the repo's root:

```
docker build -t neutrinet/matrix-alertbot:latest -f docker/Dockerfile .
```
