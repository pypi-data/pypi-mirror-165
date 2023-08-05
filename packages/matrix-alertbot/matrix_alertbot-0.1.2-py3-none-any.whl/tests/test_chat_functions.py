import unittest
from typing import Any, Dict, Optional
from unittest.mock import Mock

import nio

from matrix_alertbot.chat_functions import send_text_to_room, strip_fallback

from tests.utils import make_awaitable


async def send_room_raise_send_retry_error(
    room_id: str,
    message_type: str,
    content: Dict[Any, Any],
    tx_id: Optional[str] = None,
    ignore_unverified_devices: bool = False,
) -> nio.RoomSendResponse:
    raise nio.SendRetryError


class ChatFunctionsTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        pass

    def test_strip_fallback(self) -> None:
        fake_body = "> some message\n\nsome reply"
        message = strip_fallback(fake_body)
        self.assertEqual("some reply", message)

        fake_body = "some message"
        message = strip_fallback(fake_body)
        self.assertEqual(fake_body, message)

    async def test_send_text_to_room_as_notice(self) -> None:
        fake_response = Mock(spec=nio.RoomSendResponse)
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_matrix_client.room_send = Mock(return_value=make_awaitable(fake_response))
        fake_room_id = "!abcdefgh:example.com"
        fake_plaintext_body = "some plaintext message"
        fake_html_body = "some html message"

        response = await send_text_to_room(
            fake_matrix_client, fake_room_id, fake_plaintext_body, fake_html_body
        )

        fake_matrix_client.room_send.assert_called_once_with(
            fake_room_id,
            "m.room.message",
            {
                "msgtype": "m.notice",
                "format": "org.matrix.custom.html",
                "body": fake_plaintext_body,
                "formatted_body": fake_html_body,
            },
            ignore_unverified_devices=True,
        )
        self.assertEqual(fake_response, response)

    async def test_send_text_to_room_as_message(self) -> None:
        fake_response = Mock(spec=nio.RoomSendResponse)
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_matrix_client.room_send = Mock(return_value=make_awaitable(fake_response))
        fake_room_id = "!abcdefgh:example.com"
        fake_plaintext_body = "some plaintext message"
        fake_html_body = "some html message"

        response = await send_text_to_room(
            fake_matrix_client,
            fake_room_id,
            fake_plaintext_body,
            fake_html_body,
            notice=False,
        )

        fake_matrix_client.room_send.assert_called_once_with(
            fake_room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "body": fake_plaintext_body,
                "formatted_body": fake_html_body,
            },
            ignore_unverified_devices=True,
        )
        self.assertEqual(fake_response, response)

    async def test_send_text_to_room_in_reply_to_event(self) -> None:
        fake_response = Mock(spec=nio.RoomSendResponse)
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_matrix_client.room_send = Mock(return_value=make_awaitable(fake_response))
        fake_room_id = "!abcdefgh:example.com"
        fake_plaintext_body = "some plaintext message"
        fake_html_body = "some html message"
        fake_event_id = "some event id"

        response = await send_text_to_room(
            fake_matrix_client,
            fake_room_id,
            fake_plaintext_body,
            fake_html_body,
            reply_to_event_id=fake_event_id,
        )

        fake_matrix_client.room_send.assert_called_once_with(
            fake_room_id,
            "m.room.message",
            {
                "msgtype": "m.notice",
                "format": "org.matrix.custom.html",
                "body": fake_plaintext_body,
                "formatted_body": fake_html_body,
                "m.relates_to": {"m.in_reply_to": {"event_id": fake_event_id}},
            },
            ignore_unverified_devices=True,
        )
        self.assertEqual(fake_response, response)

    async def test_send_text_to_room_raise_send_retry_error(self) -> None:
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_matrix_client.room_send = Mock(
            side_effect=send_room_raise_send_retry_error
        )
        fake_room_id = "!abcdefgh:example.com"
        fake_plaintext_body = "some plaintext message"
        fake_html_body = "some html message"

        with self.assertRaises(nio.SendRetryError):
            await send_text_to_room(
                fake_matrix_client,
                fake_room_id,
                fake_plaintext_body,
                fake_html_body,
            )
        fake_matrix_client.room_send.assert_called_once_with(
            fake_room_id,
            "m.room.message",
            {
                "msgtype": "m.notice",
                "format": "org.matrix.custom.html",
                "body": fake_plaintext_body,
                "formatted_body": fake_html_body,
            },
            ignore_unverified_devices=True,
        )


if __name__ == "__main__":
    unittest.main()
