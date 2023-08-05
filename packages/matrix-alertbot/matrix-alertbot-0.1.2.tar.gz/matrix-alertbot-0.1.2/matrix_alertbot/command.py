import logging
from typing import Optional, Tuple

import pytimeparse2
from diskcache import Cache
from nio import AsyncClient, MatrixRoom

from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.chat_functions import send_text_to_room
from matrix_alertbot.config import Config
from matrix_alertbot.errors import (
    AlertmanagerError,
    AlertNotFoundError,
    SilenceExpiredError,
    SilenceNotFoundError,
)

logger = logging.getLogger(__name__)


class BaseCommand:
    def __init__(
        self,
        matrix_client: AsyncClient,
        cache: Cache,
        alertmanager_client: AlertmanagerClient,
        config: Config,
        room: MatrixRoom,
        sender: str,
        event_id: str,
        args: Tuple[str, ...] = None,
    ) -> None:
        """A command made by a user.

        Args:
            client: The client to communicate with Matrix.

            cache: Bot cache.

            alertmanager: The client to communicate with Alertmanager.

            config: Bot configuration parameters.

            cmd: The command and arguments.

            room: The room the command was sent in.

            sender: The sender of the event

            event_id: The ID of the event describing the command.
        """
        self.matrix_client = matrix_client
        self.cache = cache
        self.alertmanager_client = alertmanager_client
        self.config = config
        self.room = room
        self.sender = sender
        self.event_id = event_id

        if args is not None:
            self.args = args
        else:
            self.args = ()

    async def process(self) -> None:
        raise NotImplementedError


class BaseAlertCommand(BaseCommand):
    def __init__(
        self,
        client: AsyncClient,
        cache: Cache,
        alertmanager: AlertmanagerClient,
        config: Config,
        room: MatrixRoom,
        sender: str,
        event_id: str,
        reacted_to_event_id: str,
        args: Tuple[str, ...] = None,
    ) -> None:
        super().__init__(
            client, cache, alertmanager, config, room, sender, event_id, args
        )

        self.reacted_to_event_id = reacted_to_event_id


class AckAlertCommand(BaseAlertCommand):
    async def process(self) -> None:
        """Acknowledge an alert and silence it for a certain duration in Alertmanager"""
        durations = self.args
        if len(durations) > 0:
            duration = " ".join(durations)
            logger.debug(f"Receiving a command to create a silence for {duration}.")

            duration_seconds = pytimeparse2.parse(duration)
            if duration_seconds is None:
                logger.error(f"Unable to create silence: Invalid duration '{duration}'")
                await send_text_to_room(
                    self.matrix_client,
                    self.room.room_id,
                    f"I tried really hard, but I can't convert the duration '{duration}' to a number of seconds.",
                )
                return
            elif duration_seconds < 0:
                logger.error(
                    f"Unable to create silence: Duration must be positive, got '{duration}'"
                )
                await send_text_to_room(
                    self.matrix_client,
                    self.room.room_id,
                    "I can't create a silence with a negative duration!",
                )
                return
        else:
            duration_seconds = None
            logger.debug(
                "Receiving a command to create a silence for an indefinite period"
            )

        logger.debug(
            f"Reading alert fingerprint for event {self.reacted_to_event_id} from cache"
        )
        try:
            alert_fingerprint: str = self.cache[self.reacted_to_event_id]
        except KeyError:
            logger.error(
                f"Cannot find fingerprint for alert event {self.reacted_to_event_id} in cache"
            )
            return

        try:
            silence_id = await self.alertmanager_client.create_or_update_silence(
                alert_fingerprint,
                self.room.user_name(self.sender),
                duration_seconds,
                force=True,
            )
        except AlertNotFoundError as e:
            logger.warning(f"Unable to create silence: {e}")
            await send_text_to_room(
                self.matrix_client,
                self.room.room_id,
                f"Sorry, I couldn't create silence for alert with fingerprint {alert_fingerprint}: {e}",
            )
            return
        except AlertmanagerError as e:
            logger.exception(f"Unable to create silence: {e}", exc_info=e)
            await send_text_to_room(
                self.matrix_client,
                self.room.room_id,
                f"Sorry, I couldn't create silence for alert with fingerprint {alert_fingerprint} "
                f"because something went wrong with Alertmanager: {e}",
            )
            return

        self.cache.set(self.event_id, alert_fingerprint, expire=duration_seconds)

        await send_text_to_room(
            self.matrix_client,
            self.room.room_id,
            f"Created silence with ID {silence_id}.",
        )


class UnackAlertCommand(BaseAlertCommand):
    async def process(self) -> None:
        """Delete an alert's acknowledgement of an alert and remove corresponding silence in Alertmanager"""
        logger.debug("Receiving a command to delete a silence")

        logger.debug(
            f"Reading alert fingerprint for event {self.reacted_to_event_id} from cache."
        )
        try:
            alert_fingerprint: str = self.cache[self.reacted_to_event_id]
        except KeyError:
            logger.error(
                f"Cannot find fingerprint for alert event {self.reacted_to_event_id} in cache."
            )
            return
        logger.debug(f"Found alert fingerprint {alert_fingerprint} in cache.")

        logger.debug(
            f"Reading silence ID for alert fingerprint {alert_fingerprint} from cache."
        )
        try:
            silence_id: str = self.cache[alert_fingerprint]
        except KeyError:
            logger.error(
                f"Cannot find silence for alert fingerprint {alert_fingerprint} in cache"
            )
            return
        logger.debug(f"Found silence ID {silence_id} in cache.")

        logger.debug(
            f"Deleting silence with ID {silence_id} for alert with fingerprint {alert_fingerprint}"
        )

        try:
            await self.alertmanager_client.delete_silence(silence_id)
        except (SilenceNotFoundError, SilenceExpiredError) as e:
            logger.error(f"Unable to delete silence: {e}")
            await send_text_to_room(
                self.matrix_client,
                self.room.room_id,
                f"Sorry, I couldn't remove silence for alert with fingerprint {alert_fingerprint}: {e}",
            )
            return
        except AlertmanagerError as e:
            logger.exception(f"Unable to delete silence: {e}", exc_info=e)
            await send_text_to_room(
                self.matrix_client,
                self.room.room_id,
                f"Sorry, I couldn't remove silence for alert with fingerprint {alert_fingerprint} "
                f"because something went wrong with Alertmanager: {e}",
            )
            return

        self.cache.delete(alert_fingerprint)

        await send_text_to_room(
            self.matrix_client,
            self.room.room_id,
            f"Removed silence with ID {silence_id}.",
        )


class HelpCommand(BaseCommand):
    async def process(self) -> None:
        """Show the help text"""
        logger.debug(f"Displaying help to room {self.room.display_name}")
        if not self.args:
            text = (
                "Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.matrix_client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "Available commands: ..."
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.matrix_client, self.room.room_id, text)


class UnknownCommand(BaseCommand):
    async def process(self) -> None:
        logger.debug(
            f"Sending unknown command response to room {self.room.display_name}"
        )
        await send_text_to_room(
            self.matrix_client,
            self.room.room_id,
            "Unknown command. Try the 'help' command for more information.",
        )


class CommandFactory:
    @staticmethod
    def create(
        cmd: str,
        client: AsyncClient,
        cache: Cache,
        alertmanager: AlertmanagerClient,
        config: Config,
        room: MatrixRoom,
        sender: str,
        event_id: str,
        reacted_to_event_id: Optional[str] = None,
    ) -> BaseCommand:
        args = tuple(cmd.split()[1:])

        if cmd.startswith("ack"):
            if reacted_to_event_id is None:
                raise TypeError("Alert command must be in reply to an alert event.")

            return AckAlertCommand(
                client,
                cache,
                alertmanager,
                config,
                room,
                sender,
                event_id,
                reacted_to_event_id,
                args,
            )
        elif cmd.startswith("unack") or cmd.startswith("nack"):
            if reacted_to_event_id is None:
                raise TypeError("Alert command must be in reply to an alert event.")

            return UnackAlertCommand(
                client,
                cache,
                alertmanager,
                config,
                room,
                sender,
                event_id,
                reacted_to_event_id,
                args,
            )
        elif cmd.startswith("help"):
            return HelpCommand(
                client, cache, alertmanager, config, room, sender, event_id, args
            )
        else:
            return UnknownCommand(
                client, cache, alertmanager, config, room, sender, event_id, args
            )
