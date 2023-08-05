# Contributing to Matrix AlertBot

Thank you for taking interest in this little project. Below is some information
to help you with contributing.

## Setting up your development environment

See the
[Install the dependencies section of SETUP.md](SETUP.md#install-the-dependencies)
for help setting up a running environment for the bot.

### Development dependencies

There are some python dependencies that are required for linting/testing etc.
You can install them with:

```
pip install .[test]
```

## Code style

Please follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) style
guidelines and format your import statements with
[isort](https://pypi.org/project/isort/).

## Linting

Run the following script to automatically format your code. This *should* make
the linting CI happy:

```
./scripts-dev/lint.sh
```

## Testing

Run the tests with the following:

```
pytest .
```

Code coverage can be generated with:

```
coverage run --source matrix_alertbot -p -m pytest
```

Then, run either `coverage html` or `coverage lcov` to generate the report.
For html report, the results can be found in `htmlcov` directory.

## What to work on

Take a look at the [issues
list](https://gitlab.domainepublic.net/Neutrinet/matrix-alertbot/-/issues). What
feature would you like to see or bug do you want to be fixed?

If you would like to talk any ideas over before working on them, you can reach
us on our [Mattermost channel](https://chat.neutrinet.be/neutrinet/channels/hub-dev).
