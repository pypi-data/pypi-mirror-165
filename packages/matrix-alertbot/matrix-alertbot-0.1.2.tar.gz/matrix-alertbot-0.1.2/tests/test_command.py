import unittest
from typing import Dict, Optional
from unittest.mock import MagicMock, Mock, call, patch

import nio
from diskcache import Cache

import matrix_alertbot.callback
import matrix_alertbot.command
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.command import (
    AckAlertCommand,
    CommandFactory,
    HelpCommand,
    UnackAlertCommand,
    UnknownCommand,
)
from matrix_alertbot.errors import (
    AlertmanagerError,
    AlertNotFoundError,
    SilenceNotFoundError,
)

from tests.utils import make_awaitable


def cache_get_item(key: str) -> str:
    return {
        "some alert event id": "fingerprint1",
        "fingerprint1": "silence1",
    }[key]


async def create_silence(
    fingerprint: str,
    user: str,
    duration_seconds: Optional[int] = None,
    *,
    force: bool = True,
) -> str:
    if fingerprint == "fingerprint1":
        return "silence1"
    elif fingerprint == "fingerprint2":
        return "silence2"
    raise AlertmanagerError


async def create_silence_raise_alertmanager_error(
    fingerprint: str,
    user: str,
    duration_seconds: Optional[int] = None,
    *,
    force: bool = True,
) -> str:
    if fingerprint == "fingerprint1":
        raise AlertmanagerError
    return "silence1"


async def create_silence_raise_alert_not_found_error(
    fingerprint: str,
    user: str,
    duration_seconds: Optional[int] = None,
    *,
    force: bool = True,
) -> str:
    if fingerprint == "fingerprint1":
        raise AlertNotFoundError
    return "silence1"


async def delete_silence_raise_alertmanager_error(silence_id: str) -> None:
    if silence_id == "silence1":
        raise AlertmanagerError


async def delete_silence_raise_silence_not_found_error(silence_id: str) -> None:
    if silence_id == "silence1":
        raise SilenceNotFoundError


class CommandTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # Create a Command object and give it some Mock'd objects to use
        self.fake_matrix_client = Mock(spec=nio.AsyncClient)
        self.fake_matrix_client.user = "@fake_user:example.com"
        # Pretend that attempting to send a message is always successful
        self.fake_matrix_client.room_send.return_value = make_awaitable(None)

        self.fake_cache = MagicMock(spec=Cache)
        self.fake_cache.__getitem__.side_effect = cache_get_item
        self.fake_cache.__contains__.return_value = True

        self.fake_alertmanager_client = Mock(spec=AlertmanagerClient)
        self.fake_alertmanager_client.create_or_update_silence.side_effect = (
            create_silence
        )

        # Create a fake room to play with
        self.fake_room = Mock(spec=nio.MatrixRoom)
        self.fake_room.room_id = "!abcdefg:example.com"
        self.fake_room.display_name = "Fake Room"
        self.fake_room.user_name.side_effect = lambda x: x

        self.fake_event_id = "some event id"
        self.fake_sender = "@some_other_fake_user:example.com"
        self.fake_alert_event_id = "some alert event id"

        # We don't spec config, as it doesn't currently have well defined attributes
        self.fake_config = Mock()
        self.fake_config.allowed_rooms = [self.fake_room.room_id]
        self.fake_config.command_prefix = "!alert "

    @patch.object(matrix_alertbot.command.AckAlertCommand, "process")
    async def test_process_ack_command(self, fake_ack: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = CommandFactory.create(
            "ack",
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )
        await command.process()

        # Check that we attempted to process the command
        fake_ack.assert_called_once()

    @patch.object(matrix_alertbot.command.AckAlertCommand, "process")
    async def test_process_ack_with_duration_command(self, fake_ack: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = CommandFactory.create(
            "ack 1w 3d",
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )
        await command.process()

        # Check that we attempted to process the command
        fake_ack.assert_called_once()

    @patch.object(matrix_alertbot.command.UnackAlertCommand, "process")
    async def test_process_unack_command(self, fake_unack: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        for unack_cmd in ("unack", "nack"):
            command = CommandFactory.create(
                unack_cmd,
                self.fake_matrix_client,
                self.fake_cache,
                self.fake_alertmanager_client,
                self.fake_config,
                self.fake_room,
                self.fake_sender,
                self.fake_event_id,
                self.fake_alert_event_id,
            )
            await command.process()

        # Check that we attempted to process the command
        fake_unack.assert_has_calls([call(), call()])

    @patch.object(matrix_alertbot.command.HelpCommand, "process")
    async def test_process_help_command(self, fake_help: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = CommandFactory.create(
            "help",
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
        )
        await command.process()

        # Check that we attempted to process the command
        fake_help.assert_called_once()

    @patch.object(matrix_alertbot.command.UnknownCommand, "process")
    async def test_process_unknown_command(self, fake_unknown: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = CommandFactory.create(
            "",
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
        )
        await command.process()

        # Check that we attempted to process the command
        fake_unknown.assert_called_once()

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_without_duration(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {self.fake_alert_event_id: "fingerprint1"}

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_or_update_silence.assert_called_once_with(
            "fingerprint1", self.fake_sender, None, force=True
        )
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Created silence with ID silence1.",
        )
        self.fake_cache.__getitem__.assert_called_once_with(self.fake_alert_event_id)
        self.fake_cache.set.assert_called_once_with(
            "some event id", "fingerprint1", expire=None
        )

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_with_duration(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {self.fake_alert_event_id: "fingerprint1"}

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
            ("1w", "3d"),
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_or_update_silence.assert_called_once_with(
            "fingerprint1", self.fake_sender, 864000, force=True
        )
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Created silence with ID silence1.",
        )
        self.fake_cache.__getitem__.assert_called_once_with(self.fake_alert_event_id)
        self.fake_cache.set.assert_called_once_with(
            "some event id", "fingerprint1", expire=864000
        )

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_raise_alertmanager_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {
            self.fake_alert_event_id: "fingerprint1",
        }

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__
        self.fake_alertmanager_client.create_or_update_silence.side_effect = (
            create_silence_raise_alertmanager_error
        )

        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_or_update_silence.assert_called_once_with(
            "fingerprint1", self.fake_sender, None, force=True
        )
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Sorry, I couldn't create silence for alert with fingerprint fingerprint1 because something went wrong with Alertmanager: ",
        )
        self.fake_cache.__getitem__.assert_called_once_with(self.fake_alert_event_id)
        self.fake_cache.set.assert_not_called()

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_raise_alert_not_found_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {
            self.fake_alert_event_id: "fingerprint1",
        }

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__
        self.fake_alertmanager_client.create_or_update_silence.side_effect = (
            create_silence_raise_alert_not_found_error
        )

        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_or_update_silence.assert_called_once_with(
            "fingerprint1", self.fake_sender, None, force=True
        )
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Sorry, I couldn't create silence for alert with fingerprint fingerprint1: ",
        )
        self.fake_cache.__getitem__.assert_called_once_with(self.fake_alert_event_id)
        self.fake_cache.set.assert_not_called()

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_with_invalid_duration(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
            ("invalid duration",),
        )

        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_silence.assert_not_called()
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "I tried really hard, but I can't convert the duration 'invalid duration' to a number of seconds.",
        )
        self.fake_cache.__getitem__.assert_not_called()
        self.fake_cache.get.assert_not_called()
        self.fake_cache.set.assert_not_called()

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_with_negative_duration(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
            ("-1d",),
        )

        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_silence.assert_not_called()
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "I can't create a silence with a negative duration!",
        )
        self.fake_cache.__getitem__.assert_not_called()
        self.fake_cache.get.assert_not_called()
        self.fake_cache.set.assert_not_called()

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_ack_with_alert_event_not_found_in_cache(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict: Dict = {}

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__
        self.fake_cache.get.side_effect = fake_cache_dict.get

        command = AckAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )

        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.create_silence.assert_not_called()
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.__getitem__.assert_called_once_with("some alert event id")
        self.fake_cache.get.assert_not_called()
        self.fake_cache.set.assert_not_called()

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_unack(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {
            self.fake_alert_event_id: "fingerprint1",
            "fingerprint1": "silence1",
        }

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = UnackAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.delete_silence.assert_called_once_with("silence1")
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Removed silence with ID silence1.",
        )
        self.fake_cache.__getitem__.assert_has_calls(
            [call(self.fake_alert_event_id), call("fingerprint1")]
        )

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_unack_silence_raise_alertmanager_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {
            self.fake_alert_event_id: "fingerprint1",
            "fingerprint1": "silence1",
        }

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = UnackAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )

        self.fake_alertmanager_client.delete_silence.side_effect = (
            delete_silence_raise_alertmanager_error
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.delete_silence.assert_called_once_with("silence1")
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Sorry, I couldn't remove silence for alert with fingerprint fingerprint1 because something went wrong with Alertmanager: ",
        )
        self.fake_cache.__getitem__.assert_has_calls(
            [call(self.fake_alert_event_id), call("fingerprint1")]
        )

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_unack_raise_silence_not_found_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {
            self.fake_alert_event_id: "fingerprint1",
            "fingerprint1": "silence1",
        }

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = UnackAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )

        self.fake_alertmanager_client.delete_silence.side_effect = (
            delete_silence_raise_silence_not_found_error
        )
        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.delete_silence.assert_called_once_with("silence1")
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Sorry, I couldn't remove silence for alert with fingerprint fingerprint1: ",
        )
        self.fake_cache.__getitem__.assert_has_calls(
            [call(self.fake_alert_event_id), call("fingerprint1")]
        )

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_unack_with_event_not_found_in_cache(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict: Dict = {}

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = UnackAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )

        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.delete_silence.assert_not_called()
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.__getitem__.assert_called_once_with(self.fake_alert_event_id)

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_unack_with_silence_not_found_in_cache(
        self, fake_send_text_to_room: Mock
    ) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_cache_dict = {self.fake_alert_event_id: "fingerprint1"}

        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        command = UnackAlertCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            self.fake_alert_event_id,
        )

        await command.process()

        # Check that we attempted to create silences
        self.fake_alertmanager_client.delete_silence.assert_not_called()
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.__getitem__.assert_has_calls(
            [call(self.fake_alert_event_id), call("fingerprint1")]
        )

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_help_without_topic(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = HelpCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
        )

        await command.process()

        # Check that we attempted to create silences
        fake_send_text_to_room.assert_called_once()
        _, _, text = fake_send_text_to_room.call_args.args
        self.assertIn("help commands", text)

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_help_with_rules_topic(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = HelpCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            ("rules",),
        )

        await command.process()

        # Check that we attempted to create silences
        fake_send_text_to_room.assert_called_once()
        _, _, text = fake_send_text_to_room.call_args.args
        self.assertIn("rules!", text)

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_help_with_commands_topic(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = HelpCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            ("commands",),
        )

        await command.process()

        # Check that we attempted to create silences
        fake_send_text_to_room.assert_called_once()
        _, _, text = fake_send_text_to_room.call_args.args
        self.assertIn("Available commands", text)

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_help_with_unknown_topic(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = HelpCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
            ("unknown",),
        )

        await command.process()

        # Check that we attempted to create silences
        fake_send_text_to_room.assert_called_once()
        _, _, text = fake_send_text_to_room.call_args.args
        self.assertEqual("Unknown help topic!", text)

    @patch.object(matrix_alertbot.command, "send_text_to_room")
    async def test_unknown_command(self, fake_send_text_to_room: Mock) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it

        command = UnknownCommand(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            self.fake_sender,
            self.fake_event_id,
        )

        await command.process()

        # Check that we attempted to create silences
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room.room_id,
            "Unknown command. Try the 'help' command for more information.",
        )


if __name__ == "__main__":
    unittest.main()
