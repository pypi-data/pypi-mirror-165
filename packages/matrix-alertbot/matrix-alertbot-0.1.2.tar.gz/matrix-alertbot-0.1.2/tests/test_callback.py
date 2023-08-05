import unittest
from typing import Dict
from unittest.mock import MagicMock, Mock, patch

import nio
from diskcache import Cache

import matrix_alertbot.callback
import matrix_alertbot.command
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.callback import Callbacks
from matrix_alertbot.command import BaseCommand

from tests.utils import make_awaitable


class CallbacksTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # Create a Callbacks object and give it some Mock'd objects to use
        self.fake_matrix_client = Mock(spec=nio.AsyncClient)
        self.fake_matrix_client.user = "@fake_user:example.com"

        self.fake_cache = MagicMock(spec=Cache)
        self.fake_alertmanager_client = Mock(spec=AlertmanagerClient)

        # Create a fake room to play with
        self.fake_room = Mock(spec=nio.MatrixRoom)
        self.fake_room.room_id = "!abcdefg:example.com"
        self.fake_room.display_name = "Fake Room"

        # We don't spec config, as it doesn't currently have well defined attributes
        self.fake_config = Mock()
        self.fake_config.allowed_rooms = [self.fake_room.room_id]
        self.fake_config.allowed_reactions = ["🤫"]
        self.fake_config.command_prefix = "!alert "

        self.callbacks = Callbacks(
            self.fake_matrix_client,
            self.fake_alertmanager_client,
            self.fake_cache,
            self.fake_config,
        )

    async def test_invite(self) -> None:
        """Tests the callback for InviteMemberEvents"""
        # Tests that the bot attempts to join a room after being invited to it
        fake_invite_event = Mock(spec=nio.InviteMemberEvent)
        fake_invite_event.sender = "@some_other_fake_user:example.com"

        # Pretend that attempting to join a room is always successful
        self.fake_matrix_client.join.return_value = make_awaitable(None)

        # Pretend that we received an invite event
        await self.callbacks.invite(self.fake_room, fake_invite_event)

        # Check that we attempted to join the room
        self.fake_matrix_client.join.assert_called_once_with(self.fake_room.room_id)

    @patch.object(matrix_alertbot.callback.CommandFactory, "create", autospec=True)
    async def test_message_without_prefix(self, fake_command_create: Mock) -> None:
        """Tests the callback for RoomMessageText without any command prefix"""
        # Tests that the bot process messages in the room
        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "Hello world!"

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that the command was not executed
        fake_command_create.assert_not_called()

    @patch.object(matrix_alertbot.command, "HelpCommand", autospec=True)
    async def test_message_help_not_in_reply_with_prefix(
        self, fake_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.event_id = "some event id"
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "!alert help"
        fake_message_event.source = {"content": {}}

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that the command was not executed
        fake_command.assert_called_with(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            fake_message_event.sender,
            fake_message_event.event_id,
            (),
        )
        fake_command.return_value.process.assert_called_once()

    @patch.object(matrix_alertbot.command, "HelpCommand", autospec=True)
    async def test_message_help_in_reply_with_prefix(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command

        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.event_id = "some event id"
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "!alert help"
        fake_message_event.source = {
            "content": {
                "m.relates_to": {"m.in_reply_to": {"event_id": "some alert event id"}}
            }
        }

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that we attempted to execute the command
        fake_command.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            fake_message_event.sender,
            fake_message_event.event_id,
            (),
        )
        fake_command.return_value.process.assert_called_once()

    @patch.object(matrix_alertbot.command.CommandFactory, "create", autospec=True)
    async def test_ignore_message_sent_by_bot(self, fake_create_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command

        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.sender = self.fake_matrix_client.user

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that we attempted to execute the command
        fake_create_command.assert_not_called()

    @patch.object(matrix_alertbot.command.CommandFactory, "create", autospec=True)
    async def test_ignore_message_sent_on_unauthorized_room(
        self, fake_create_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command

        self.fake_room.room_id = "!unauthorizedroom@example.com"

        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.sender = "@some_other_fake_user:example.com"

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that we attempted to execute the command
        fake_create_command.assert_not_called()

    @patch.object(matrix_alertbot.command, "AckAlertCommand", autospec=True)
    async def test_message_ack_not_in_reply_with_prefix(
        self, fake_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.event_id = "some event id"
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "!alert ack"
        fake_message_event.source = {"content": {}}

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that the command was not executed
        fake_command.assert_not_called()

    @patch.object(matrix_alertbot.command, "AckAlertCommand", autospec=True)
    async def test_message_ack_in_reply_with_prefix(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.event_id = "some event id"
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "!alert ack"
        fake_message_event.source = {
            "content": {
                "m.relates_to": {"m.in_reply_to": {"event_id": "some alert event id"}}
            }
        }

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that the command was not executed
        fake_command.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            fake_message_event.sender,
            fake_message_event.event_id,
            "some alert event id",
            (),
        )
        fake_command.return_value.process.assert_called_once()

    @patch.object(matrix_alertbot.callback, "UnackAlertCommand", autospec=True)
    async def test_message_unack_not_in_reply_with_prefix(
        self, fake_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.event_id = "some event id"
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "!alert unack"
        fake_message_event.source = {"content": {}}

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that the command was not executed
        fake_command.assert_not_called()

    @patch.object(matrix_alertbot.command, "UnackAlertCommand", autospec=True)
    async def test_message_unack_in_reply_with_prefix(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_message_event = Mock(spec=nio.RoomMessageText)
        fake_message_event.event_id = "some event id"
        fake_message_event.sender = "@some_other_fake_user:example.com"
        fake_message_event.body = "!alert unack"
        fake_message_event.source = {
            "content": {
                "m.relates_to": {"m.in_reply_to": {"event_id": "some alert event id"}}
            }
        }

        # Pretend that we received a text message event
        await self.callbacks.message(self.fake_room, fake_message_event)

        # Check that the command was not executed
        fake_command.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            fake_message_event.sender,
            fake_message_event.event_id,
            "some alert event id",
            (),
        )
        fake_command.return_value.process.assert_called_once()

    @patch.object(matrix_alertbot.callback, "AckAlertCommand", autospec=True)
    async def test_reaction_to_existing_alert(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_alert_event = Mock(spec=nio.RoomMessageText)
        fake_alert_event.event_id = "some alert event id"
        fake_alert_event.sender = self.fake_config.user_id

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = "@some_other_fake_user:example.com"
        fake_reaction_event.source = {
            "content": {
                "m.relates_to": {
                    "event_id": fake_alert_event.event_id,
                    "key": "🤫",
                    "rel_type": "m.annotation",
                }
            }
        }

        fake_event_response = Mock(spec=nio.RoomGetEventResponse)
        fake_event_response.event = fake_alert_event
        self.fake_matrix_client.room_get_event.return_value = make_awaitable(
            fake_event_response
        )

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            fake_reaction_event.sender,
            fake_reaction_event.event_id,
            "some alert event id",
        )
        fake_command.return_value.process.assert_called_once()
        self.fake_matrix_client.room_get_event.assert_called_once_with(
            self.fake_room.room_id, fake_alert_event.event_id
        )

    @patch.object(matrix_alertbot.callback, "AckAlertCommand", autospec=True)
    async def test_reaction_to_inexistent_event(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_alert_event_id = "some alert event id"

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = "@some_other_fake_user:example.com"
        fake_reaction_event.source = {
            "content": {
                "m.relates_to": {
                    "event_id": fake_alert_event_id,
                    "key": "🤫",
                    "rel_type": "m.annotation",
                }
            }
        }

        fake_event_response = Mock(spec=nio.RoomGetEventError)
        self.fake_matrix_client.room_get_event.return_value = make_awaitable(
            fake_event_response
        )

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_matrix_client.room_get_event.assert_called_once_with(
            self.fake_room.room_id, fake_alert_event_id
        )

    @patch.object(matrix_alertbot.callback, "AckAlertCommand", autospec=True)
    async def test_reaction_to_event_not_from_bot_user(
        self, fake_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_alert_event = Mock(spec=nio.RoomMessageText)
        fake_alert_event.event_id = "some alert event id"
        fake_alert_event.sender = "@some_other_fake_user.example.com"

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = "@some_other_fake_user:example.com"
        fake_reaction_event.source = {
            "content": {
                "m.relates_to": {
                    "event_id": fake_alert_event.event_id,
                    "key": "🤫",
                    "rel_type": "m.annotation",
                }
            }
        }

        fake_event_response = Mock(spec=nio.RoomGetEventResponse)
        fake_event_response.event = fake_alert_event
        self.fake_matrix_client.room_get_event.return_value = make_awaitable(
            fake_event_response
        )

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_matrix_client.room_get_event.assert_called_once_with(
            self.fake_room.room_id, fake_alert_event.event_id
        )

    @patch.object(matrix_alertbot.callback, "AckAlertCommand", autospec=True)
    async def test_reaction_unknown(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_alert_event_id = "some alert event id"

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = "@some_other_fake_user:example.com"
        fake_reaction_event.source = {
            "content": {
                "m.relates_to": {
                    "event_id": fake_alert_event_id,
                    "key": "unknown",
                    "rel_type": "m.annotation",
                }
            }
        }

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_matrix_client.room_get_event.assert_not_called()

    @patch.object(matrix_alertbot.callback, "AckAlertCommand", autospec=True)
    async def test_ignore_reaction_sent_by_bot_user(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_alert_event_id = "some alert event id"

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = self.fake_matrix_client.user
        fake_reaction_event.source = {
            "content": {
                "m.relates_to": {
                    "event_id": fake_alert_event_id,
                    "key": "unknown",
                    "rel_type": "m.annotation",
                }
            }
        }

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)
        await self.callbacks._reaction(
            self.fake_room, fake_reaction_event, fake_alert_event_id
        )

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_matrix_client.room_get_event.assert_not_called()

    @patch.object(matrix_alertbot.callback, "AckAlertCommand", autospec=True)
    async def test_ignore_reaction_in_unauthorized_room(
        self, fake_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        self.fake_room.room_id = "!unauthorizedroom@example.com"

        fake_alert_event_id = "some alert event id"

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = "@some_other_fake_user:example.com"
        fake_reaction_event.source = {
            "content": {
                "m.relates_to": {
                    "event_id": fake_alert_event_id,
                    "key": "unknown",
                    "rel_type": "m.annotation",
                }
            }
        }

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)
        await self.callbacks._reaction(
            self.fake_room, fake_reaction_event, fake_alert_event_id
        )

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_matrix_client.room_get_event.assert_not_called()

    @patch.object(matrix_alertbot.callback, "UnackAlertCommand", autospec=True)
    async def test_redaction(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_alert_event_id = "some alert event id"

        fake_redaction_event = Mock(spec=nio.RedactionEvent)
        fake_redaction_event.redacts = "some other event id"
        fake_redaction_event.event_id = "some event id"
        fake_redaction_event.sender = "@some_other_fake_user:example.com"

        fake_cache_dict = {fake_redaction_event.redacts: fake_alert_event_id}
        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        # Pretend that we received a text message event
        await self.callbacks.redaction(self.fake_room, fake_redaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_cache,
            self.fake_alertmanager_client,
            self.fake_config,
            self.fake_room,
            fake_redaction_event.sender,
            fake_redaction_event.event_id,
            fake_redaction_event.redacts,
        )
        fake_command.return_value.process.assert_called_once()

    @patch.object(matrix_alertbot.callback, "UnackAlertCommand", autospec=True)
    async def test_ignore_redaction_sent_by_bot_user(self, fake_command: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_redaction_event = Mock(spec=nio.RedactionEvent)
        fake_redaction_event.sender = self.fake_matrix_client.user

        fake_cache_dict: Dict = {}
        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        # Pretend that we received a text message event
        await self.callbacks.redaction(self.fake_room, fake_redaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_cache.__getitem__.assert_not_called()

    @patch.object(matrix_alertbot.callback, "UnackAlertCommand", autospec=True)
    async def test_ignore_redaction_in_unauthorized_room(
        self, fake_command: Mock
    ) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        self.fake_room.room_id = "!unauthorizedroom@example.com"

        fake_redaction_event = Mock(spec=nio.RedactionEvent)
        fake_redaction_event.sender = "@some_other_fake_user:example.com"

        fake_cache_dict: Dict = {}
        self.fake_cache.__getitem__.side_effect = fake_cache_dict.__getitem__

        # Pretend that we received a text message event
        await self.callbacks.redaction(self.fake_room, fake_redaction_event)

        # Check that we attempted to execute the command
        fake_command.assert_not_called()
        self.fake_cache.__getitem__.assert_not_called()

    @patch.object(matrix_alertbot.callback.CommandFactory, "create", autospec=True)
    async def test_unknown(self, fake_command_create: Mock) -> None:
        """Tests the callback for RoomMessageText with the command prefix"""
        # Tests that the bot process messages in the room that contain a command
        fake_command = Mock(spec=BaseCommand)
        fake_command_create.return_value = fake_command

        fake_reaction_event = Mock(spec=nio.UnknownEvent)
        fake_reaction_event.type = "m.reaction"
        fake_reaction_event.event_id = "some event id"
        fake_reaction_event.sender = "@some_other_fake_user:example.com"
        fake_reaction_event.source = {}

        # Pretend that we received a text message event
        await self.callbacks.unknown(self.fake_room, fake_reaction_event)

        # Check that we attempted to execute the command
        fake_command_create.assert_not_called()


if __name__ == "__main__":
    unittest.main()
