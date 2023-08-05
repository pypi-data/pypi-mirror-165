import logging

from diskcache import Cache
from nio import (
    AsyncClient,
    InviteMemberEvent,
    JoinError,
    LocalProtocolError,
    MatrixRoom,
    MegolmEvent,
    RedactionEvent,
    RoomGetEventError,
    RoomMessageText,
    SendRetryError,
    UnknownEvent,
)

from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.chat_functions import strip_fallback
from matrix_alertbot.command import AckAlertCommand, CommandFactory, UnackAlertCommand
from matrix_alertbot.config import Config

logger = logging.getLogger(__name__)


class Callbacks:
    def __init__(
        self,
        matrix_client: AsyncClient,
        alertmanager_client: AlertmanagerClient,
        cache: Cache,
        config: Config,
    ):
        """
        Args:
            client: nio client used to interact with matrix.

            cache: Bot cache.

            alertmanager: Client used to interact with alertmanager.

            config: Bot configuration parameters.
        """
        self.matrix_client = matrix_client
        self.cache = cache
        self.alertmanager_client = alertmanager_client
        self.config = config
        self.command_prefix = config.command_prefix

    async def message(self, room: MatrixRoom, event: RoomMessageText) -> None:
        """Callback for when a message event is received

        Args:
            room: The room the event came from.

            event: The event defining the message.
        """
        # Ignore messages from ourselves
        if event.sender == self.matrix_client.user:
            return

        # Ignore messages from unauthorized room
        if room.room_id not in self.config.allowed_rooms:
            return

        # Extract the message text
        msg = strip_fallback(event.body)

        logger.debug(
            f"Bot message received for room {room.display_name} | "
            f"{room.user_name(event.sender)}: {msg}"
        )
        # Process as message if in a public room without command prefix
        has_command_prefix = msg.startswith(self.command_prefix)
        if not has_command_prefix:
            logger.debug(
                f"Cannot process message: Command prefix {self.command_prefix} not provided."
            )
            return

        source_content = event.source["content"]
        reacted_to_event_id = (
            source_content.get("m.relates_to", {})
            .get("m.in_reply_to", {})
            .get("event_id")
        )

        if reacted_to_event_id is not None:
            logger.debug(f"Command in reply to event ID {reacted_to_event_id}")

        # Remove the command prefix
        cmd = msg[len(self.command_prefix) :]
        try:
            command = CommandFactory.create(
                cmd,
                self.matrix_client,
                self.cache,
                self.alertmanager_client,
                self.config,
                room,
                event.sender,
                event.event_id,
                reacted_to_event_id,
            )
        except TypeError as e:
            logging.error(f"Cannot process command '{cmd}': {e}")
            return

        try:
            await command.process()
        except (SendRetryError, LocalProtocolError) as e:
            logger.exception(f"Unable to send message to {room.room_id}", exc_info=e)

    async def invite(self, room: MatrixRoom, event: InviteMemberEvent) -> None:
        """Callback for when an invite is received. Join the room specified in the invite.

        Args:
            room: The room that we are invited to.

            event: The invite event.
        """
        # Ignore invites from unauthorized room
        if room.room_id not in self.config.allowed_rooms:
            return

        logger.debug(f"Got invite to {room.room_id} from {event.sender}.")

        # Attempt to join 3 times before giving up
        for attempt in range(3):
            result = await self.matrix_client.join(room.room_id)
            if type(result) == JoinError:
                logger.error(
                    f"Error joining room {room.room_id} (attempt %d): %s",
                    attempt,
                    result.message,
                )
            else:
                break
        else:
            logger.error("Unable to join room: %s", room.room_id)

        # Successfully joined room
        logger.info(f"Joined {room.room_id}")

    async def invite_event_filtered_callback(
        self, room: MatrixRoom, event: InviteMemberEvent
    ) -> None:
        """
        Since the InviteMemberEvent is fired for every m.room.member state received
        in a sync response's `rooms.invite` section, we will receive some that are
        not actually our own invite event (such as the inviter's membership).
        This makes sure we only call `callbacks.invite` with our own invite events.
        """
        if event.state_key == self.matrix_client.user_id:
            # This is our own membership (invite) event
            await self.invite(room, event)

    async def _reaction(
        self, room: MatrixRoom, event: UnknownEvent, alert_event_id: str
    ) -> None:
        """A reaction was sent to one of our messages. Let's send a reply acknowledging it.

        Args:
            room: The room the reaction was sent in.

            event: The reaction event.

            reacted_to_id: The event ID that the reaction points to.
        """
        # Ignore reactions from unauthorized room
        if room.room_id not in self.config.allowed_rooms:
            return

        # Ignore reactions from ourselves
        if event.sender == self.matrix_client.user:
            return

        reaction = event.source.get("content", {}).get("m.relates_to", {}).get("key")
        logger.debug(f"Got reaction {reaction} to {room.room_id} from {event.sender}.")

        if reaction not in self.config.allowed_reactions:
            logger.warning(f"Uknown duration reaction {reaction}")
            return

        # Get the original event that was reacted to
        event_response = await self.matrix_client.room_get_event(
            room.room_id, alert_event_id
        )
        if isinstance(event_response, RoomGetEventError):
            logger.warning(
                f"Error getting event that was reacted to ({alert_event_id})"
            )
            return
        reacted_to_event = event_response.event

        # Only acknowledge reactions to events that we sent
        if reacted_to_event.sender != self.config.user_id:
            return

        # Send a message acknowledging the reaction
        command = AckAlertCommand(
            self.matrix_client,
            self.cache,
            self.alertmanager_client,
            self.config,
            room,
            event.sender,
            event.event_id,
            alert_event_id,
        )

        try:
            await command.process()
        except (SendRetryError, LocalProtocolError) as e:
            logger.exception(f"Unable to send message to {room.room_id}", exc_info=e)

    async def redaction(self, room: MatrixRoom, event: RedactionEvent) -> None:
        # Ignore events from unauthorized room
        if room.room_id not in self.config.allowed_rooms:
            return

        # Ignore redactions from ourselves
        if event.sender == self.matrix_client.user:
            return

        logger.debug(f"Received event to remove event ID {event.redacts}")

        command = UnackAlertCommand(
            self.matrix_client,
            self.cache,
            self.alertmanager_client,
            self.config,
            room,
            event.sender,
            event.event_id,
            event.redacts,
        )
        try:
            await command.process()
        except (SendRetryError, LocalProtocolError) as e:
            logger.exception(f"Unable to send message to {room.room_id}", exc_info=e)

    async def decryption_failure(self, room: MatrixRoom, event: MegolmEvent) -> None:
        """Callback for when an event fails to decrypt. Inform the user.

        Args:
            room: The room that the event that we were unable to decrypt is in.

            event: The encrypted event that we were unable to decrypt.
        """
        # Ignore events from unauthorized room
        if room.room_id not in self.config.allowed_rooms:
            return

        logger.error(
            f"Failed to decrypt event '{event.event_id}' in room '{room.room_id}'!"
            f"\n\n"
            f"Tip: try using a different device ID in your config file and restart."
            f"\n\n"
            f"If all else fails, delete your store directory and let the bot recreate "
            f"it (your reminders will NOT be deleted, but the bot may respond to existing "
            f"commands a second time)."
        )

    async def unknown(self, room: MatrixRoom, event: UnknownEvent) -> None:
        """Callback for when an event with a type that is unknown to matrix-nio is received.
        Currently this is used for reaction events, which are not yet part of a released
        matrix spec (and are thus unknown to nio).

        Args:
            room: The room the reaction was sent in.

            event: The event itself.
        """
        # Ignore events from unauthorized room
        if room.room_id not in self.config.allowed_rooms:
            return

        if event.type == "m.reaction":
            # Get the ID of the event this was a reaction to
            relation_dict = event.source.get("content", {}).get("m.relates_to", {})

            reacted_to_id = relation_dict.get("event_id")
            if reacted_to_id and relation_dict.get("rel_type") == "m.annotation":
                await self._reaction(room, event, reacted_to_id)
                return

        logger.debug(
            f"Got unknown event with type to {event.type} from {event.sender} in {room.room_id}."
        )
