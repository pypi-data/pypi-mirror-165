import os
import unittest
from datetime import timedelta
from unittest.mock import Mock, patch

import yaml

from matrix_alertbot.config import DEFAULT_REACTIONS, Config
from matrix_alertbot.errors import (
    InvalidConfigError,
    ParseConfigError,
    RequiredConfigKeyError,
)

WORKING_DIR = os.path.dirname(__file__)
CONFIG_RESOURCES_DIR = os.path.join(WORKING_DIR, "resources", "config")


class DummyConfig(Config):
    def __init__(self, filepath: str):
        with open(filepath) as file_stream:
            self.config_dict = yaml.safe_load(file_stream.read())


def mock_path_isdir(path: str) -> bool:
    if path == "data/store":
        return False
    return True


def mock_path_exists(path: str) -> bool:
    if path == "data/store":
        return False
    return True


class ConfigTestCase(unittest.TestCase):
    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_read_minimal_config(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = Config(config_path)

        fake_path_isdir.assert_called_once_with("data/store")
        fake_path_exists.assert_called_once_with("data/store")
        fake_mkdir.assert_called_once_with("data/store")

        self.assertEqual("@fakes_user:matrix.example.com", config.user_id)
        self.assertEqual("password", config.user_password)
        self.assertIsNone(config.user_token)
        self.assertIsNone(config.device_id)
        self.assertEqual("matrix-alertbot", config.device_name)
        self.assertEqual("https://matrix.example.com", config.homeserver_url)
        self.assertEqual(["!abcdefgh:matrix.example.com"], config.allowed_rooms)
        self.assertEqual(DEFAULT_REACTIONS, config.allowed_reactions)

        self.assertEqual("0.0.0.0", config.address)
        self.assertEqual(8080, config.port)
        self.assertIsNone(config.socket)

        self.assertEqual("http://localhost:9093", config.alertmanager_url)

        expected_expire_time = timedelta(days=7).total_seconds()
        self.assertEqual(expected_expire_time, config.cache_expire_time)
        self.assertEqual("data/cache", config.cache_dir)

        self.assertEqual("data/store", config.store_dir)

        self.assertIsNone(config.template_dir)

        self.assertEqual("!alert ", config.command_prefix)

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_read_full_config(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.full.yml")
        config = Config(config_path)

        fake_path_isdir.assert_called_once_with("data/store")
        fake_path_exists.assert_called_once_with("data/store")
        fake_mkdir.assert_called_once_with("data/store")

        self.assertEqual("@fakes_user:matrix.example.com", config.user_id)
        self.assertEqual("password", config.user_password)
        self.assertIsNone(config.user_token)
        self.assertEqual("ABCDEFGHIJ", config.device_id)
        self.assertEqual("fake_device_name", config.device_name)
        self.assertEqual("https://matrix.example.com", config.homeserver_url)
        self.assertEqual(["!abcdefgh:matrix.example.com"], config.allowed_rooms)
        self.assertEqual({"🤫", "😶", "🤐"}, config.allowed_reactions)

        self.assertIsNone(config.address)
        self.assertIsNone(config.port)
        self.assertEqual("matrix-alertbot.socket", config.socket)

        self.assertEqual("http://localhost:9093", config.alertmanager_url)

        expected_expire_time = timedelta(days=7).total_seconds()
        self.assertEqual(expected_expire_time, config.cache_expire_time)
        self.assertEqual("data/cache", config.cache_dir)

        self.assertEqual("data/store", config.store_dir)

        self.assertEqual("data/templates", config.template_dir)

        self.assertEqual("!alert ", config.command_prefix)

    def test_read_config_raise_config_error(self) -> None:
        with self.assertRaises(ParseConfigError):
            Config("")

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_storage_path_error(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = True

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        with self.assertRaises(ParseConfigError):
            Config(config_path)

        fake_path_isdir.assert_called_once_with("data/store")
        fake_path_exists.assert_called_once_with("data/store")
        fake_mkdir.assert_not_called()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_matrix_user_id(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["matrix"]["user_id"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_matrix_user_password(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["matrix"]["user_password"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_matrix_url(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["matrix"]["url"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_matrix_allowed_rooms(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["matrix"]["allowed_rooms"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_webhook_address(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["webhook"]["address"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_alertmanager_url(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["alertmanager"]["url"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_cache_path(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["cache"]["path"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_missing_storage_path(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        del config.config_dict["storage"]["path"]

        with self.assertRaises(RequiredConfigKeyError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_invalid_matrix_user_id(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)

        config.config_dict["matrix"]["user_id"] = ""
        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()

        config.config_dict["matrix"]["user_id"] = "@fake_user"
        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()

        config.config_dict["matrix"]["user_id"] = "@fake_user:"
        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()

        config.config_dict["matrix"]["user_id"] = ":matrix.example.com"
        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()

        config.config_dict["matrix"]["user_id"] = "@:matrix.example.com"
        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()

        config.config_dict["matrix"]["user_id"] = "@:"
        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()

    @patch("os.path.isdir")
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_parse_config_with_both_webhook_socket_and_address(
        self, fake_mkdir: Mock, fake_path_exists: Mock, fake_path_isdir: Mock
    ) -> None:
        fake_path_isdir.return_value = False
        fake_path_exists.return_value = False

        config_path = os.path.join(CONFIG_RESOURCES_DIR, "config.minimal.yml")
        config = DummyConfig(config_path)
        config.config_dict["webhook"]["socket"] = "matrix-alertbot.socket"

        with self.assertRaises(InvalidConfigError):
            config._parse_config_values()


if __name__ == "__main__":
    unittest.main()
