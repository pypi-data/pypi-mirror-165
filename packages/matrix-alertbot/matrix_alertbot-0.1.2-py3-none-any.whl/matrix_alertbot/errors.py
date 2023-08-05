# This file holds custom error types that you can define for your application.


class ConfigError(Exception):
    """An error encountered during reading the config file."""

    pass


class ParseConfigError(ConfigError):
    """An error encountered when config file cannot be parsed."""

    pass


class InvalidConfigError(ParseConfigError):
    """An error encountered when a config key is not valid."""

    pass


class RequiredConfigKeyError(ConfigError):
    """An error encountered when a required config key is missing."""

    pass


class AlertmanagerError(Exception):
    """An error encountered with Alertmanager."""

    pass


class AlertNotFoundError(AlertmanagerError):
    """An error encountered when an alert cannot be found in Alertmanager."""

    pass


class SilenceNotFoundError(AlertmanagerError):
    """An error encountered when a silence cannot be found in Alertmanager."""

    pass


class SilenceExpiredError(AlertmanagerError):
    """An error encountered when a silence is already expired in Alertmanager."""

    pass


class SilenceExtendError(AlertmanagerError):
    """An error encountered when a silence cannot be extended."""

    pass


class AlertmanagerServerError(AlertmanagerError):
    """An error encountered with Alertmanager server."""

    pass
