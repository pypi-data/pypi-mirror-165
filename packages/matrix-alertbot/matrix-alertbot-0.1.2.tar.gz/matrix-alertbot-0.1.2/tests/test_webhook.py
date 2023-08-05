import unittest
from typing import Dict
from unittest.mock import Mock, call, patch

import aiohttp.test_utils
import nio
from aiohttp import web
from diskcache import Cache
from nio import LocalProtocolError, RoomSendResponse

import matrix_alertbot.webhook
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.config import Config
from matrix_alertbot.errors import (
    AlertmanagerError,
    SilenceExtendError,
    SilenceNotFoundError,
)
from matrix_alertbot.webhook import Webhook


def send_text_to_room_raise_error(
    client: nio.AsyncClient, room_id: str, plaintext: str, html: str, notice: bool
) -> RoomSendResponse:
    raise LocalProtocolError


def update_silence_raise_silence_not_found(fingerprint: str) -> str:
    raise SilenceNotFoundError


def update_silence_raise_silence_extend_error(fingerprint: str) -> str:
    raise SilenceExtendError


def update_silence_raise_alertmanager_error(fingerprint: str) -> str:
    raise AlertmanagerError


class WebhookApplicationTestCase(aiohttp.test_utils.AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        self.fake_matrix_client = Mock(spec=nio.AsyncClient)
        self.fake_alertmanager_client = Mock(spec=AlertmanagerClient)
        self.fake_cache = Mock(spec=Cache)

        self.fake_room_id = "!abcdefg:example.com"

        self.fake_config = Mock(spec=Config)
        self.fake_config.port = aiohttp.test_utils.unused_port()
        self.fake_config.address = "localhost"
        self.fake_config.socket = "webhook.sock"
        self.fake_config.allowed_rooms = [self.fake_room_id]
        self.fake_config.cache_expire_time = 0
        self.fake_config.template_dir = None

        self.fake_alerts = {
            "alerts": [
                {
                    "fingerprint": "fingerprint1",
                    "generatorURL": "http://example.com/alert1",
                    "status": "firing",
                    "labels": {
                        "alertname": "alert1",
                        "severity": "critical",
                        "job": "job1",
                    },
                    "annotations": {"description": "some description1"},
                },
                {
                    "fingerprint": "fingerprint2",
                    "generatorURL": "http://example.com/alert2",
                    "status": "resolved",
                    "labels": {
                        "alertname": "alert2",
                        "severity": "warning",
                        "job": "job2",
                    },
                    "annotations": {"description": "some description2"},
                },
            ]
        }

        webhook = Webhook(
            self.fake_matrix_client,
            self.fake_alertmanager_client,
            self.fake_cache,
            self.fake_config,
        )
        return webhook.app

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_with_silence_not_found(
        self, fake_send_text_to_room: Mock
    ) -> None:
        self.fake_alertmanager_client.update_silence.side_effect = (
            update_silence_raise_silence_not_found
        )

        data = self.fake_alerts
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(200, response.status)

        self.fake_alertmanager_client.update_silence.assert_called_once_with(
            "fingerprint1"
        )
        self.assertEqual(2, fake_send_text_to_room.call_count)
        fake_send_text_to_room.assert_has_calls(
            [
                call(
                    self.fake_matrix_client,
                    self.fake_room_id,
                    "[🔥 CRITICAL] alert1: some description1",
                    '<font color="#dc3545">\n  <b>[🔥 CRITICAL]</b>\n</font> '
                    '<a href="http://example.com/alert1">alert1</a>\n (job1)<br/>\n'
                    "some description1",
                    notice=False,
                ),
                call(
                    self.fake_matrix_client,
                    self.fake_room_id,
                    "[🥦 RESOLVED] alert2: some description2",
                    '<font color="#33cc33">\n  <b>[🥦 RESOLVED]</b>\n</font> '
                    '<a href="http://example.com/alert2">alert2</a>\n (job2)<br/>\n'
                    "some description2",
                    notice=False,
                ),
            ]
        )
        self.fake_cache.set.assert_called_once_with(
            fake_send_text_to_room.return_value.event_id,
            "fingerprint1",
            expire=self.fake_config.cache_expire_time,
        )
        self.assertEqual(2, self.fake_cache.delete.call_count)
        self.fake_cache.delete.assert_has_calls(
            [call("fingerprint1"), call("fingerprint2")]
        )

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_with_silence_extend_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        self.fake_alertmanager_client.update_silence.side_effect = (
            update_silence_raise_silence_extend_error
        )

        data = self.fake_alerts
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(200, response.status)

        self.fake_alertmanager_client.update_silence.assert_called_once_with(
            "fingerprint1"
        )
        self.assertEqual(2, fake_send_text_to_room.call_count)
        fake_send_text_to_room.assert_has_calls(
            [
                call(
                    self.fake_matrix_client,
                    self.fake_room_id,
                    "[🔥 CRITICAL] alert1: some description1",
                    '<font color="#dc3545">\n  <b>[🔥 CRITICAL]</b>\n</font> '
                    '<a href="http://example.com/alert1">alert1</a>\n (job1)<br/>\n'
                    "some description1",
                    notice=False,
                ),
                call(
                    self.fake_matrix_client,
                    self.fake_room_id,
                    "[🥦 RESOLVED] alert2: some description2",
                    '<font color="#33cc33">\n  <b>[🥦 RESOLVED]</b>\n</font> '
                    '<a href="http://example.com/alert2">alert2</a>\n (job2)<br/>\n'
                    "some description2",
                    notice=False,
                ),
            ]
        )
        self.fake_cache.set.assert_called_once_with(
            fake_send_text_to_room.return_value.event_id,
            "fingerprint1",
            expire=self.fake_config.cache_expire_time,
        )
        self.fake_cache.delete.assert_called_once_with("fingerprint2")

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_with_alertmanager_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        self.fake_alertmanager_client.update_silence.side_effect = (
            update_silence_raise_alertmanager_error
        )

        data = self.fake_alerts
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(500, response.status)

        self.fake_alertmanager_client.update_silence.assert_called_once_with(
            "fingerprint1"
        )
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_not_called()

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_with_existing_silence(
        self, fake_send_text_to_room: Mock
    ) -> None:
        self.fake_alertmanager_client.update_silence.return_value = "silence1"

        data = self.fake_alerts
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(200, response.status)

        self.fake_alertmanager_client.update_silence.assert_called_once_with(
            "fingerprint1"
        )
        fake_send_text_to_room.assert_called_once_with(
            self.fake_matrix_client,
            self.fake_room_id,
            "[🥦 RESOLVED] alert2: some description2",
            '<font color="#33cc33">\n  <b>[🥦 RESOLVED]</b>\n</font> '
            '<a href="http://example.com/alert2">alert2</a>\n (job2)<br/>\n'
            "some description2",
            notice=False,
        )
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_called_once_with("fingerprint2")

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_in_unauthorized_room(
        self, fake_send_text_to_room: Mock
    ) -> None:
        room_id = "!unauthorized_room@example.com"
        async with self.client.request(
            "POST", f"/alerts/{room_id}", json=self.fake_alerts
        ) as response:
            self.assertEqual(401, response.status)
            error_msg = await response.text()

        self.assertEqual(
            "Cannot send alerts to room ID !unauthorized_room@example.com.", error_msg
        )
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_not_called()

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_with_empty_data(
        self, fake_send_text_to_room: Mock
    ) -> None:
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json={}
        ) as response:
            self.assertEqual(400, response.status)
            error_msg = await response.text()

        self.assertEqual("Data must contain 'alerts' key.", error_msg)
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_not_called()

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_empty_alerts(self, fake_send_text_to_room: Mock) -> None:
        data: Dict = {"alerts": []}
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(400, response.status)
            error_msg = await response.text()

        self.assertEqual("Alerts cannot be empty.", error_msg)
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_not_called()

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_invalid_alerts(self, fake_send_text_to_room: Mock) -> None:
        data = {"alerts": "invalid"}
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(400, response.status)
            error_msg = await response.text()

        self.assertEqual("Alerts must be a list, got 'str'.", error_msg)
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_not_called()

    @patch.object(matrix_alertbot.webhook, "send_text_to_room")
    async def test_post_alerts_with_empty_items(
        self, fake_send_text_to_room: Mock
    ) -> None:
        data: Dict = {"alerts": [{}]}
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(400, response.status)
            error_msg = await response.text()

        self.assertEqual("Invalid alert: {}.", error_msg)
        fake_send_text_to_room.assert_not_called()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_not_called()

    @patch.object(
        matrix_alertbot.webhook,
        "send_text_to_room",
        side_effect=send_text_to_room_raise_error,
    )
    async def test_post_alerts_raise_send_error(
        self, fake_send_text_to_room: Mock
    ) -> None:
        self.fake_alertmanager_client.update_silence.side_effect = (
            update_silence_raise_silence_not_found
        )

        data = self.fake_alerts
        async with self.client.request(
            "POST", f"/alerts/{self.fake_room_id}", json=data
        ) as response:
            self.assertEqual(500, response.status)
            error_msg = await response.text()

        self.assertEqual(
            "An error occured when sending alert with fingerprint 'fingerprint1' to Matrix room.",
            error_msg,
        )
        fake_send_text_to_room.assert_called_once()
        self.fake_cache.set.assert_not_called()
        self.fake_cache.delete.assert_called_once_with("fingerprint1")

    async def test_health(self) -> None:
        async with self.client.request("GET", "/health") as response:
            self.assertEqual(200, response.status)

    async def test_metrics(self) -> None:
        async with self.client.request("GET", "/metrics") as response:
            self.assertEqual(200, response.status)


class WebhookServerTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.fake_matrix_client = Mock(spec=nio.AsyncClient)
        self.fake_alertmanager_client = Mock(spec=AlertmanagerClient)
        self.fake_cache = Mock(spec=Cache)

        self.fake_config = Mock(spec=Config)
        self.fake_config.port = aiohttp.test_utils.unused_port()
        self.fake_config.address = "localhost"
        self.fake_config.socket = "webhook.sock"
        self.fake_config.cache_expire_time = 0
        self.fake_config.template_dir = None

    @patch.object(matrix_alertbot.webhook.web, "TCPSite", autospec=True)
    async def test_webhook_start_address_port(self, fake_tcp_site: Mock) -> None:
        webhook = Webhook(
            self.fake_matrix_client,
            self.fake_alertmanager_client,
            self.fake_cache,
            self.fake_config,
        )
        await webhook.start()

        fake_tcp_site.assert_called_once_with(
            webhook.runner, self.fake_config.address, self.fake_config.port
        )

        await webhook.close()

    @patch.object(matrix_alertbot.webhook.web, "UnixSite", autospec=True)
    async def test_webhook_start_unix_socket(self, fake_unix_site: Mock) -> None:
        self.fake_config.address = None
        self.fake_config.port = None

        webhook = Webhook(
            self.fake_matrix_client,
            self.fake_alertmanager_client,
            self.fake_cache,
            self.fake_config,
        )
        await webhook.start()

        fake_unix_site.assert_called_once_with(webhook.runner, self.fake_config.socket)

        await webhook.close()
