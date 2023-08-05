from __future__ import annotations

import logging

import prometheus_client
from aiohttp import ClientError, web, web_request
from aiohttp_prometheus_exporter.handler import metrics
from aiohttp_prometheus_exporter.middleware import prometheus_middleware_factory
from diskcache import Cache
from nio import AsyncClient, LocalProtocolError, SendRetryError

from matrix_alertbot.alert import Alert, AlertRenderer
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.chat_functions import send_text_to_room
from matrix_alertbot.config import Config
from matrix_alertbot.errors import (
    AlertmanagerError,
    SilenceExtendError,
    SilenceNotFoundError,
)

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get("/health")
async def get_health(request: web_request.Request) -> web.Response:
    return web.Response(status=200)


@routes.post("/alerts/{room_id}")
async def create_alerts(request: web_request.Request) -> web.Response:
    data = await request.json()
    room_id = request.match_info["room_id"]

    config: Config = request.app["config"]

    if room_id not in config.allowed_rooms:
        logger.error("Cannot send alerts to room ID {room_id}.")
        return web.Response(
            status=401, body=f"Cannot send alerts to room ID {room_id}."
        )

    if "alerts" not in data:
        logger.error("Received data without 'alerts' key")
        return web.Response(status=400, body="Data must contain 'alerts' key.")

    alert_dicts = data["alerts"]

    if not isinstance(data["alerts"], list):
        alerts_type = type(alert_dicts).__name__
        logger.error(f"Received data with invalid alerts type '{alerts_type}'.")
        return web.Response(
            status=400, body=f"Alerts must be a list, got '{alerts_type}'."
        )

    logger.info(f"Received {len(alert_dicts)} alerts for room ID {room_id}: {data}")

    if len(data["alerts"]) == 0:
        return web.Response(status=400, body="Alerts cannot be empty.")

    alerts = []
    for alert in alert_dicts:
        try:
            alert = Alert.from_dict(alert)
        except KeyError as e:
            logger.error(f"Cannot parse alert dict: {e}")
            return web.Response(status=400, body=f"Invalid alert: {alert}.")
        alerts.append(alert)

    for alert in alerts:
        try:
            await create_alert(alert, room_id, request)
        except AlertmanagerError as e:
            logger.error(
                f"An error occured with Alertmanager when handling alert with fingerprint {alert.fingerprint}: {e}"
            )
            return web.Response(
                status=500,
                body=f"An error occured with Alertmanager when handling alert with fingerprint {alert.fingerprint}.",
            )
        except (SendRetryError, LocalProtocolError, ClientError) as e:
            logger.error(
                f"Unable to send alert {alert.fingerprint} to Matrix room: {e}"
            )
            return web.Response(
                status=500,
                body=f"An error occured when sending alert with fingerprint '{alert.fingerprint}' to Matrix room.",
            )

    return web.Response(status=200)


async def create_alert(
    alert: Alert, room_id: str, request: web_request.Request
) -> None:
    alertmanager_client: AlertmanagerClient = request.app["alertmanager_client"]
    alert_renderer: AlertRenderer = request.app["alert_renderer"]
    matrix_client: AsyncClient = request.app["matrix_client"]
    cache: Cache = request.app["cache"]
    config: Config = request.app["config"]

    if alert.firing:
        try:
            silence_id = await alertmanager_client.update_silence(alert.fingerprint)
            logger.debug(
                f"Extended silence ID {silence_id} for alert with fingerprint {alert.fingerprint}"
            )
            return
        except SilenceNotFoundError as e:
            logger.debug(
                f"Unable to extend silence for alert with fingerprint {alert.fingerprint}: {e}"
            )
            cache.delete(alert.fingerprint)
        except SilenceExtendError as e:
            logger.debug(
                f"Unable to extend silence for alert with fingerprint {alert.fingerprint}: {e}"
            )

    plaintext = alert_renderer.render(alert, html=False)
    html = alert_renderer.render(alert, html=True)

    event = await send_text_to_room(
        matrix_client, room_id, plaintext, html, notice=False
    )

    if alert.firing:
        cache.set(event.event_id, alert.fingerprint, expire=config.cache_expire_time)
    else:
        cache.delete(alert.fingerprint)


class Webhook:
    def __init__(
        self,
        matrix_client: AsyncClient,
        alertmanager_client: AlertmanagerClient,
        cache: Cache,
        config: Config,
    ) -> None:
        self.app = web.Application(logger=logger)
        self.app["matrix_client"] = matrix_client
        self.app["alertmanager_client"] = alertmanager_client
        self.app["config"] = config
        self.app["cache"] = cache
        self.app["alert_renderer"] = AlertRenderer(config.template_dir)
        self.app.add_routes(routes)

        prometheus_registry = prometheus_client.CollectorRegistry(auto_describe=True)
        self.app.middlewares.append(
            prometheus_middleware_factory(registry=prometheus_registry)
        )
        self.app.router.add_get("/metrics", metrics())

        self.runner = web.AppRunner(self.app)

        self.config = config
        self.address = config.address
        self.port = config.port
        self.socket = config.socket

    async def start(self) -> None:
        await self.runner.setup()

        site: web.BaseSite
        if self.address and self.port:
            site = web.TCPSite(self.runner, self.address, self.port)
            logger.info(f"Listening on {self.address}:{self.port}")
        elif self.socket:
            site = web.UnixSite(self.runner, self.socket)
            logger.info(f"Listening on unix://{self.socket}")

        await site.start()

    async def close(self) -> None:
        await self.runner.cleanup()
