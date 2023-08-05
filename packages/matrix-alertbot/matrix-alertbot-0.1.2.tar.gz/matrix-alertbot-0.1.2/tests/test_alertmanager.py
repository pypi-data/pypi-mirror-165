from __future__ import annotations

import json
import unittest
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple
from unittest.mock import Mock, patch

import aiohttp
import aiohttp.test_utils
import aiotools
from aiohttp import web, web_request
from diskcache import Cache
from freezegun import freeze_time

import matrix_alertbot.alertmanager
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.errors import (
    AlertmanagerServerError,
    AlertNotFoundError,
    SilenceExpiredError,
    SilenceExtendError,
    SilenceNotFoundError,
)


async def update_silence_raise_silence_not_found(
    fingerprint: str, user: str, duration_seconds: int, *, force: bool = False
) -> str:
    raise SilenceNotFoundError


class FakeCache:
    def __init__(self, cache_dict: Optional[Dict] = None) -> None:
        if cache_dict is None:
            cache_dict = {}
        self.cache = cache_dict

    def get(
        self, key: str, expire_time: bool = False
    ) -> Optional[Tuple[str, Optional[int]] | str]:
        return self.cache.get(key)

    def set(self, key: str, value: str, expire: int) -> None:
        self.cache[key] = value, expire


class AbstractFakeAlertmanagerServer:
    def __init__(self) -> None:
        self.app = web.Application()
        self.app.router.add_routes(
            [
                web.get("/api/v2/alerts", self.get_alerts),
                web.get("/api/v2/silences", self.get_silences),
                web.post("/api/v2/silences", self.create_silence),
                web.delete("/api/v2/silence/{silence}", self.delete_silence),
            ]
        )
        self.app["silences"] = [
            {
                "id": "silence1",
                "createdBy": "user1",
                "status": {"state": "active"},
                "matchers": [],
            },
            {
                "id": "silence2",
                "createdBy": "user2",
                "status": {"state": "expired"},
                "matchers": [],
            },
        ]

        self.runner = web.AppRunner(self.app)

    async def __aenter__(self) -> AbstractFakeAlertmanagerServer:
        await self.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.stop()

    async def start(self) -> None:
        self.port = aiohttp.test_utils.unused_port()

        await self.runner.setup()

        site = web.TCPSite(self.runner, "127.0.0.1", self.port)
        await site.start()

    async def stop(self) -> None:
        await self.runner.cleanup()

    async def get_alerts(self, request: web_request.Request) -> web.Response:
        raise NotImplementedError

    async def get_silences(self, request: web_request.Request) -> web.Response:
        raise NotImplementedError

    async def create_silence(self, request: web_request.Request) -> web.Response:
        raise NotImplementedError

    async def delete_silence(self, request: web_request.Request) -> web.Response:
        raise NotImplementedError


class FakeAlertmanagerServer(AbstractFakeAlertmanagerServer):
    async def get_alerts(self, request: web_request.Request) -> web.Response:
        return web.Response(
            body=json.dumps(
                [
                    {
                        "fingerprint": "fingerprint1",
                        "labels": {"alertname": "alert1"},
                        "status": {"state": "active"},
                    },
                    {
                        "fingerprint": "fingerprint2",
                        "labels": {"alertname": "alert2"},
                        "status": {
                            "state": "suppressed",
                            "silencedBy": ["silence1", "silence2"],
                        },
                    },
                ]
            ),
            content_type="application/json",
        )

    async def get_silences(self, request: web_request.Request) -> web.Response:
        return web.Response(
            body=json.dumps(self.app["silences"]), content_type="application/json"
        )

    async def create_silence(self, request: web_request.Request) -> web.Response:
        silences = self.app["silences"]

        silence = await request.json()

        silence_count = len(silences) + 1
        silence["id"] = f"silence{silence_count}"
        silence["status"] = {"state": "active"}
        silences.append(silence)

        return web.Response(
            body=json.dumps({"silenceID": silence["id"]}),
            content_type="application/json",
        )

    async def delete_silence(self, request: web_request.Request) -> web.Response:
        silence_id = request.match_info["silence"]
        for i, silence in enumerate(self.app["silences"]):
            if silence["id"] == silence_id:
                del self.app["silences"][i]
                break

        return web.Response(status=200, content_type="application/json")


class FakeAlertmanagerServerWithoutAlert(FakeAlertmanagerServer):
    async def get_alerts(self, request: web_request.Request) -> web.Response:
        return web.Response(body=json.dumps([]), content_type="application/json")


class FakeAlertmanagerServerWithErrorAlerts(FakeAlertmanagerServer):
    async def get_alerts(self, request: web_request.Request) -> web.Response:
        return web.Response(status=500)


class FakeAlertmanagerServerWithoutSilence(FakeAlertmanagerServer):
    def __init__(self) -> None:
        super().__init__()
        self.app["silences"] = []


class FakeAlertmanagerServerWithErrorSilences(FakeAlertmanagerServer):
    async def get_silences(self, request: web_request.Request) -> web.Response:
        return web.Response(status=500)


class FakeAlertmanagerServerWithErrorCreateSilence(FakeAlertmanagerServer):
    async def create_silence(self, request: web_request.Request) -> web.Response:
        return web.Response(status=500)


class FakeAlertmanagerServerWithErrorDeleteSilence(FakeAlertmanagerServer):
    async def delete_silence(self, request: web_request.Request) -> web.Response:
        return web.Response(status=500)


class AlertmanagerClientTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.fake_fingerprints = Mock(return_value=["fingerprint1", "fingerprint2"])

    async def test_get_alerts_happy(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServer() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                alerts = await alertmanager_client.get_alerts()

        self.assertEqual(
            [
                {
                    "fingerprint": "fingerprint1",
                    "labels": {"alertname": "alert1"},
                    "status": {"state": "active"},
                },
                {
                    "fingerprint": "fingerprint2",
                    "labels": {"alertname": "alert2"},
                    "status": {
                        "state": "suppressed",
                        "silencedBy": ["silence1", "silence2"],
                    },
                },
            ],
            alerts,
        )

    async def test_get_alerts_empty(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutAlert() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                alerts = await alertmanager_client.get_alerts()

        self.assertEqual([], alerts)

    async def test_get_alerts_raise_alertmanager_error(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithErrorAlerts() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.get_alerts()

    async def test_get_silences_happy(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServer() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silences = await alertmanager_client.get_silences()

        self.assertEqual(
            [
                {
                    "id": "silence1",
                    "createdBy": "user1",
                    "status": {"state": "active"},
                    "matchers": [],
                },
                {
                    "id": "silence2",
                    "createdBy": "user2",
                    "status": {"state": "expired"},
                    "matchers": [],
                },
            ],
            silences,
        )

    async def test_get_silences_empty(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silences = await alertmanager_client.get_silences()

        self.assertEqual([], silences)

    async def test_get_silences_raise_alertmanager_error(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithErrorSilences() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.get_silences()

    async def test_get_alert_happy(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServer() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                alert = await alertmanager_client.get_alert("fingerprint1")

        self.assertEqual(
            {
                "fingerprint": "fingerprint1",
                "labels": {"alertname": "alert1"},
                "status": {"state": "active"},
            },
            alert,
        )

    async def test_get_alert_raise_alert_not_found(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutAlert() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(AlertNotFoundError):
                    await alertmanager_client.get_alert("fingerprint1")

    async def test_get_alert_raise_alertmanager_error(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithErrorAlerts() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.get_alert("fingerprint1")

    async def test_get_silence_happy(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServer() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silence1 = await alertmanager_client.get_silence("silence1")
                silence2 = await alertmanager_client.get_silence("silence2")

        self.assertEqual(
            {
                "id": "silence1",
                "createdBy": "user1",
                "status": {"state": "active"},
                "matchers": [],
            },
            silence1,
        )
        self.assertEqual(
            {
                "id": "silence2",
                "createdBy": "user2",
                "status": {"state": "expired"},
                "matchers": [],
            },
            silence2,
        )

    async def test_get_silence_raise_silence_not_found(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(SilenceNotFoundError):
                    await alertmanager_client.get_silence("silence1")

    async def test_get_silence_raise_alertmanager_error(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithErrorSilences() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.get_silence("silence1")

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_create_silence_with_duration(self) -> None:
        fake_cache = Mock(return_value=FakeCache())

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silence_id = await alertmanager_client.create_silence(
                    "fingerprint1", "user", 86400
                )
                silence = await alertmanager_client.get_silence("silence1")

        self.assertEqual("silence1", silence_id)
        self.assertEqual(
            {
                "id": "silence1",
                "status": {"state": "active"},
                "matchers": [
                    {
                        "name": "alertname",
                        "value": "alert1",
                        "isRegex": False,
                        "isEqual": True,
                    }
                ],
                "createdBy": "user",
                "startsAt": "1970-01-01T00:00:00",
                "endsAt": "1970-01-02T00:00:00",
                "comment": "Acknowledge alert from Matrix",
            },
            silence,
        )
        fake_cache.set.assert_called_once_with("fingerprint1", "silence1", expire=86400)

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_update_silence_raise_extend_error(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                await alertmanager_client.create_silence("fingerprint1", "user", 86400)
                with self.assertRaises(SilenceExtendError):
                    await alertmanager_client.update_silence("fingerprint1")
                with self.assertRaises(SilenceNotFoundError):
                    await alertmanager_client.get_silence("silence2")
        self.assertEqual({"fingerprint1": ("silence1", 86400)}, fake_cache.cache)

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_update_silence_remove_duration(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silence_id1 = await alertmanager_client.create_silence(
                    "fingerprint1", "user", 86400
                )
                silence_id2 = await alertmanager_client.update_silence(
                    "fingerprint1", force=True
                )
                silence2 = await alertmanager_client.get_silence("silence2")

        self.assertEqual("silence1", silence_id1)
        self.assertEqual("silence2", silence_id2)
        self.assertEqual(
            {
                "id": "silence2",
                "status": {"state": "active"},
                "matchers": [
                    {
                        "name": "alertname",
                        "value": "alert1",
                        "isRegex": False,
                        "isEqual": True,
                    }
                ],
                "createdBy": "user",
                "startsAt": "1970-01-01T00:00:00",
                "endsAt": "1970-01-01T03:00:00",
                "comment": "Acknowledge alert from Matrix",
            },
            silence2,
        )
        self.assertEqual({"fingerprint1": ("silence2", None)}, fake_cache.cache)

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_update_silence_override_user_and_duration(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                await alertmanager_client.create_silence("fingerprint1", "user1", 86400)
                silence_id2 = await alertmanager_client.update_silence(
                    "fingerprint1", "user2", 864000
                )
                silence2 = await alertmanager_client.get_silence("silence2")

        self.assertEqual("silence2", silence_id2)
        self.assertEqual(
            {
                "id": "silence2",
                "status": {"state": "active"},
                "matchers": [
                    {
                        "name": "alertname",
                        "value": "alert1",
                        "isRegex": False,
                        "isEqual": True,
                    }
                ],
                "createdBy": "user2",
                "startsAt": "1970-01-01T00:00:00",
                "endsAt": "1970-01-11T00:00:00",
                "comment": "Acknowledge alert from Matrix",
            },
            silence2,
        )
        self.assertEqual({"fingerprint1": ("silence2", 864000)}, fake_cache.cache)

    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "update_silence")
    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "create_silence")
    async def test_create_or_update_silence_with_duration_and_silence_not_found(
        self, fake_create_silence: Mock, fake_update_silence: Mock
    ) -> None:
        fake_cache = Mock(spec=Cache)
        fake_update_silence.side_effect = update_silence_raise_silence_not_found
        fake_create_silence.return_value = "silence1"

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)
        async with aiotools.closing_async(alertmanager_client):
            silence_id1 = await alertmanager_client.create_or_update_silence(
                "fingerprint1", "user", 86400
            )

        self.assertEqual("silence1", silence_id1)
        fake_update_silence.assert_called_once_with(
            "fingerprint1", "user", 86400, force=False
        )
        fake_create_silence.assert_called_once_with("fingerprint1", "user", 86400)

    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "update_silence")
    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "create_silence")
    async def test_create_or_update_silence_with_duration_and_silence_found(
        self, fake_create_silence: Mock, fake_update_silence: Mock
    ) -> None:
        fake_cache = Mock(spec=Cache)
        fake_update_silence.return_value = "silence1"

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)
        async with aiotools.closing_async(alertmanager_client):
            silence_id1 = await alertmanager_client.create_or_update_silence(
                "fingerprint1", "user", 86400
            )

        self.assertEqual("silence1", silence_id1)
        fake_update_silence.assert_called_once_with(
            "fingerprint1", "user", 86400, force=False
        )
        fake_create_silence.assert_not_called()

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_create_silence_without_duration(self) -> None:
        fake_cache = Mock(spec=Cache)
        fake_cache.get.return_value = None

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silence_id = await alertmanager_client.create_silence(
                    "fingerprint1", "user"
                )
                silence = await alertmanager_client.get_silence("silence1")

        self.assertEqual("silence1", silence_id)
        self.assertEqual(
            {
                "id": "silence1",
                "status": {"state": "active"},
                "matchers": [
                    {
                        "name": "alertname",
                        "value": "alert1",
                        "isRegex": False,
                        "isEqual": True,
                    }
                ],
                "createdBy": "user",
                "startsAt": "1970-01-01T00:00:00",
                "endsAt": "1970-01-01T03:00:00",
                "comment": "Acknowledge alert from Matrix",
            },
            silence,
        )
        fake_cache.set.assert_called_once_with("fingerprint1", "silence1", expire=None)

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_update_silence_without_duration(self) -> None:
        fake_cache = FakeCache()

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silence1_id = await alertmanager_client.create_silence(
                    "fingerprint1", "user"
                )
                silence2_id = await alertmanager_client.update_silence("fingerprint1")
                silence = await alertmanager_client.get_silence("silence2")

        self.assertEqual("silence1", silence1_id)
        self.assertEqual("silence2", silence2_id)
        self.assertEqual(
            {
                "id": "silence2",
                "status": {"state": "active"},
                "matchers": [
                    {
                        "name": "alertname",
                        "value": "alert1",
                        "isRegex": False,
                        "isEqual": True,
                    }
                ],
                "createdBy": "user",
                "startsAt": "1970-01-01T00:00:00",
                "endsAt": "1970-01-01T03:00:00",
                "comment": "Acknowledge alert from Matrix",
            },
            silence,
        )
        self.assertEqual({"fingerprint1": ("silence2", None)}, fake_cache.cache)

    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "update_silence")
    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "create_silence")
    async def test_create_or_update_silence_without_duration_and_silence_not_found(
        self, fake_create_silence: Mock, fake_update_silence: Mock
    ) -> None:
        fake_cache = Mock(spec=Cache)
        fake_update_silence.side_effect = update_silence_raise_silence_not_found
        fake_create_silence.return_value = "silence1"

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)
        async with aiotools.closing_async(alertmanager_client):
            silence_id1 = await alertmanager_client.create_or_update_silence(
                "fingerprint1", "user"
            )

        self.assertEqual("silence1", silence_id1)
        fake_update_silence.assert_called_once_with(
            "fingerprint1", "user", None, force=False
        )
        fake_create_silence.assert_called_once_with("fingerprint1", "user", None)

    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "update_silence")
    @patch.object(matrix_alertbot.alertmanager.AlertmanagerClient, "create_silence")
    async def test_create_or_update_silence_without_duration_and_silence_found(
        self, fake_create_silence: Mock, fake_update_silence: Mock
    ) -> None:
        fake_cache = Mock(spec=Cache)
        fake_update_silence.return_value = "silence1"

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)
        async with aiotools.closing_async(alertmanager_client):
            silence_id1 = await alertmanager_client.create_or_update_silence(
                "fingerprint1", "user"
            )

        self.assertEqual("silence1", silence_id1)
        fake_update_silence.assert_called_once_with(
            "fingerprint1", "user", None, force=False
        )
        fake_create_silence.assert_not_called()

    @freeze_time(datetime.utcfromtimestamp(0))
    async def test_create_silence_with_max_duration(self) -> None:
        fake_cache = Mock(spec=Cache)
        fake_cache.get.return_value = None
        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                silence_id = await alertmanager_client.create_silence(
                    "fingerprint1", "user", int(timedelta.max.total_seconds()) + 1
                )
                silence = await alertmanager_client.get_silence("silence1")

        self.assertEqual("silence1", silence_id)
        self.assertEqual(
            {
                "id": "silence1",
                "status": {"state": "active"},
                "matchers": [
                    {
                        "name": "alertname",
                        "value": "alert1",
                        "isRegex": False,
                        "isEqual": True,
                    }
                ],
                "createdBy": "user",
                "startsAt": "1970-01-01T00:00:00",
                "endsAt": "1980-01-01T00:00:00",
                "comment": "Acknowledge alert from Matrix",
            },
            silence,
        )

    async def test_create_silence_raise_alert_not_found(self) -> None:
        fake_cache = Mock(spec=Cache)
        fake_cache.get.return_value = None

        async with FakeAlertmanagerServerWithoutAlert() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(AlertNotFoundError):
                    await alertmanager_client.create_silence("fingerprint1", "user")

    async def test_create_silence_raise_alertmanager_error(self) -> None:
        fake_cache = Mock(spec=Cache)
        fake_cache.get.return_value = None

        async with FakeAlertmanagerServerWithErrorCreateSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                await alertmanager_client.get_alert("fingerprint1")

                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.create_silence("fingerprint1", "user")

    async def test_update_silence_raise_silence_not_found(self) -> None:
        fake_cache = FakeCache({"fingerprint1": ("silence1", None)})

        async with FakeAlertmanagerServerWithoutSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(SilenceNotFoundError):
                    await alertmanager_client.update_silence("fingerprint1")
                with self.assertRaises(SilenceNotFoundError):
                    await alertmanager_client.update_silence("fingerprint2")

    async def test_update_silence_raise_silence_extend_error(self) -> None:
        fake_cache = FakeCache({"fingerprint1": ("silence1", 86400)})

        async with FakeAlertmanagerServerWithoutAlert() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(SilenceExtendError):
                    await alertmanager_client.update_silence("fingerprint1")

    async def test_update_silence_raise_alertmanager_error(self) -> None:
        fake_cache = FakeCache({"fingerprint1": ("silence1", None)})

        async with FakeAlertmanagerServerWithErrorCreateSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                await alertmanager_client.get_alert("fingerprint1")

                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.update_silence("fingerprint1")

    async def test_delete_silence(self) -> None:
        fake_cache = Mock(spec=Cache)

        async with FakeAlertmanagerServer() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                await alertmanager_client.delete_silence("silence1")
                silences = await alertmanager_client.get_silences()

        self.assertEqual(
            [
                {
                    "id": "silence2",
                    "createdBy": "user2",
                    "status": {"state": "expired"},
                    "matchers": [],
                }
            ],
            silences,
        )

    async def test_delete_silence_raise_silence_expired(self) -> None:
        fake_cache = Mock(spec=Cache)

        async with FakeAlertmanagerServer() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                with self.assertRaises(SilenceExpiredError):
                    await alertmanager_client.delete_silence("silence2")
                silences = await alertmanager_client.get_silences()

        self.assertEqual(2, len(silences))

    async def test_delete_silence_raise_alertmanager_error(self) -> None:
        fake_cache = Mock(spec=Cache)

        async with FakeAlertmanagerServerWithErrorDeleteSilence() as fake_alertmanager_server:
            port = fake_alertmanager_server.port
            alertmanager_client = AlertmanagerClient(
                f"http://localhost:{port}", fake_cache
            )
            async with aiotools.closing_async(alertmanager_client):
                await alertmanager_client.get_alert("fingerprint1")

                with self.assertRaises(AlertmanagerServerError):
                    await alertmanager_client.delete_silence("silence1")

    async def test_find_alert_happy(self) -> None:
        fake_cache = Mock(spec=Cache)

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)
        alert = alertmanager_client._find_alert(
            "fingerprint1", [{"fingerprint": "fingerprint1"}]
        )
        self.assertEqual({"fingerprint": "fingerprint1"}, alert)

    async def test_find_alert_raise_alert_not_found(self) -> None:
        fake_cache = Mock(spec=Cache)

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)

        with self.assertRaises(AlertNotFoundError):
            alertmanager_client._find_alert("fingerprint1", [])

        with self.assertRaises(AlertNotFoundError):
            alertmanager_client._find_alert(
                "fingerprint2", [{"fingerprint": "fingerprint1"}]
            )

    async def test_find_silence_happy(self) -> None:
        fake_cache = Mock(spec=Cache)

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)
        silence = alertmanager_client._find_silence("silence1", [{"id": "silence1"}])
        self.assertEqual({"id": "silence1"}, silence)

    async def test_find_silence_raise_silence_not_found(self) -> None:
        fake_cache = Mock(spec=Cache)

        alertmanager_client = AlertmanagerClient("http://localhost", fake_cache)

        with self.assertRaises(SilenceNotFoundError):
            alertmanager_client._find_silence("silence1", [])

        with self.assertRaises(SilenceNotFoundError):
            alertmanager_client._find_silence("silence2", [{"id": "silence1"}])


if __name__ == "__main__":
    unittest.main()
