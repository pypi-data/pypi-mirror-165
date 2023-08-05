# Matrix AlertBot [![Built with matrix-nio](https://img.shields.io/badge/built%20with-matrix--nio-brightgreen)](https://github.com/poljar/matrix-nio) [![coverage report](https://gitlab.domainepublic.net/Neutrinet/matrix-alertbot/badges/master/coverage.svg)](https://gitlab.domainepublic.net/Neutrinet/matrix-alertbot/-/commits/master) 

A bot that receives alert from [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager) to send them to a Matrix room. Users can interract with the bot to create silences for the alerts.

Features include:

* Send alerts from Alertmanager to a Matrix room
* Add a reaction to an alert to create a silence until the alert is resolved
* Reply to an alert to create a silence with a given duration
* Reply to an alert to create a silence until the alert is resolved
* Remove silences created through the bot
* Participation in end-to-end encrypted rooms

## Getting started

See [SETUP.md](SETUP.md) for how to setup and run the bot.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to the project.

## Project structure

The majority of the code is kept inside of the `matrix_alertbot` folder, which
is in itself a [python package](https://docs.python.org/3/tutorial/modules.html), 
the `__init__.py` file inside declaring it as such.

To run the bot, the `matrix-alertbot` script in the root of the codebase is
available. It will import the `main` function from the `main.py` file in the
package and run it. To properly install this script into your python environment, 
run `pip install -e .` in the project's root directory.

`setup.py` contains package information (for publishing the code to
[PyPI](https://pypi.org)) and `setup.cfg` just contains some configuration
options for linting tools.

`config.sample.yaml` is a sample configuration file. You should copy this file to `config.yaml` , then edit it according to
your needs. Be sure never to check the edited `config.yaml` into source control
since it'll likely contain sensitive details such as passwords!
