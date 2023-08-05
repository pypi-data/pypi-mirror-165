# Setup

Matrix AlertBot is a sample repository of a working Matrix bot that can be taken
and transformed into one's own bot, service or whatever else may be necessary.
Below is a quick setup guide to running the existing bot.

## Install the dependencies

There are two paths to installing the dependencies for development.

### Using `docker-compose`

Docker Compose is the easiest way to run the bot with all the necessary dependencies handled for you.

After installation and ensuring the `docker-compose` command works, you need to:

1. Create a data directory and config file by following the
   [docker setup instructions](docker/README.md#setup).

2. Create a docker volume pointing to that directory:

   

```
   docker volume create \
     --opt type=none \
     --opt o=bind \
     --opt device="/path/to/data/dir" data_volume
   ```

Run `docker-compose up --build` to start the bot.

### Running natively

If you would rather not or are unable to run docker, the following will
instruct you on how to install the dependencies natively:

#### Install libolm

You can install [libolm](https://gitlab.matrix.org/matrix-org/olm) from source, 
or alternatively, check your system's package manager. Version `3.0.0` or
greater is required.

#### Deploy Alertmanager and Prometheus

Matrix AlertBot requires an Alertmanager instance to manage silences, receive alerts from it, etc. You can follow install instructions on the [Alertmanager website](https://prometheus.io/docs/alerting/latest/alertmanager).

Prometheus is also required in order to setup a set of rules that will trigger alerts. You can follow install instructions on the [Prometheus website](https://prometheus.io/docs/prometheus/latest/getting_started/)

Sample configs are available in the `docker` directory.

#### Install Python dependencies

Create and activate a Python 3 virtual environment:

```
virtualenv -p python3 .venv
source env/bin/activate
```

Install python dependencies:

```
pip install -e .
```

(Optional) If you want to send alert to encrypted rooms, use the following
command to install olm dependencies alongside those that are necessary:

```
pip install -e ".[e2e]"
```

## Configuration

Copy the sample configuration file to a new `config.yaml` file.

```
cp config.sample.yaml config.yaml
```

Edit the config file. The `matrix` section must be modified at least.

## Running

### Docker

Refer to the docker [run instructions](docker/README.md#running).

### Native installation

Make sure to source your python environment if you haven't already:

```
source .venv/bin/activate
```

Then simply run the bot with:

```
matrix-alertbot
```

By default, the bot will run with the config file at `./config.yaml` . However, an
alternative relative or absolute filepath can be specified after the command:

```
matrix-alertbot other-config.yaml
```

## Testing the bot works

Invite the bot to a room and it should accept the invite and join.

Matrix AlertBot will process any message starting with the prefix defined in the config. By default, this prefix is `!alert` . Let's test this now.
After the bot has successfully joined the room, try sending the following
in a message:

```
!alert help
```

The bot should reply with an help message, explaining how to handle alerts.

When an alert is triggered, the bot will send it to the room.
You can manage silences for this alert either by replying to the message, 
or by reacting with certain emojis.

For instance, if you reply to the alert with:

```
!alert ack
```

This will create a silence for this alert until it is resolved.

You can at any moment reply to the alert with the following to remove the 
silence:

```
!alert unack
```

Removing a reaction to an alert will also remove the silence.

## Troubleshooting

If you had any difficulties with this setup process, please [file an
issue](https://gitlab.domainepublic.net/Neutrinet/matrix-alertbot/-/issues) or come talk
about it in [the Mattermost channel](https://chat.neutrinet.be/neutrinet/channels/hub-dev).
