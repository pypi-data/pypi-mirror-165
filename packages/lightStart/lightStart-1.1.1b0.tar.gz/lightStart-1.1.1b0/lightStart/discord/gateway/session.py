from base64 import b64encode
from datetime import datetime
from json import dumps, loads
from random import randint
from sys import exc_info
from threading import Thread
from time import perf_counter
from typing import Optional

from websocket import WebSocketApp

from lightStart.discord.gateway.argument_handler import Parse_Args
from lightStart.discord.gateway.codes import EVENTS, OPCODES
from lightStart.utils.shared import data


class WebSocket:
    """The WebSocket class is used for interacting with the Discord gateway. It handles connecting to and resuming connections to the gateway. It also handles all events the gateway sends.

    Attributes:
        Client (Instance): The class used for interacting with the Discord API. More information about the class can be found in the docstring for the ‘Instance’ class in ‘/src/discord/client.py’.
        connected (bool): Tells the program whether there is an active gateway session.
        heartbeat_interval (NoneType / int): The time in seconds between each heartbeat the program should send, or ‘None’ if it has not been received yet. Without heartbeats, the gateway session would get invalidated around a minute after it is created.
        last_seq (NoneType / int): The last sequence number the program received from the gateway, or ‘None’ if it has not been received yet. This is used when resuming previous gateway connections.
        reconnect (bool): Tells the program whether to make a new gateway connection, or to resume a previous one.
        session_id (NoneType / int): The ID of the gateway connection, or ‘None’ if none have been established yet. This is used when resuming previous gateway connections.

    Methods:
        session_start() -> None
        on_open() -> None
        on_message(event: str) -> None
        on_error(error: str) -> None
        on_close(close_code: Optional[int] = None, close_msg: Optional[str] = None) -> None
        cmd_handler(event: dict) -> Optional[bool]
        decompress(event: str) -> dict
        send(payload: dict) -> None
        send_heartbeat() -> None
    """

    def __init__(self, Client) -> None:
        self.Client = Client

        self.connected = False
        self.heartbeat_interval = None
        self.last_heartbeat = None
        self.last_seq = None
        self.reconnect = False
        self.session_id = None

        self.session_start()

        self.send_heartbeat()  # Start the heartbeat sender.

    def session_start(self) -> None:
        """Initializes the connection to the Discord gateway.

        Args:
            NONE

        Returns:
            NoneType

        """

        url = f"wss://gateway.discord.gg/?v={self.Client.api_version}&encoding=json"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "json",
            "Accept-Language": "en-GB,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive, Upgrade",
            "Host": "gateway.discord.gg",
            "Origin": "https://discord.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "websocket",
            "Sec-Fetch-Mode": "websocket",
            "Sec-Fetch-Site": "cross-site",
            "Sec-WebSocket-Extensions": "permessage-deflate",
            "Sec-WebSocket-Key": f"{b64encode(''.join([chr(randint(32, 127)) for _ in range(16)]).encode('ascii')).decode()}",
            "Sec-Websocket-Vesion": "13",
            "Upgrade": "websocket",
            "User_Agent": f"{self.Client.user_agent}",
        }

        self.ws = WebSocketApp(
            url,
            header=headers,
            on_open=lambda ws: self.on_open(),
            on_message=lambda ws, msg: self.on_message(msg),
            on_error=lambda ws, msg: self.on_error(msg),
            on_close=lambda ws, close_code, close_msg: self.on_close(
                close_code, close_msg
            ),
        )  # Initialize the WebSocket class.
        Thread(target=self.ws.run_forever).start()  # Connect to the gateway.
        
        self.connected = True

    def on_open(self) -> None:
        """Authenticates the gateway session and starts the proper session.

        Args:
            NONE

        Returns:
            NoneType

        """
        
        if (
            self.reconnect and self.session_id is not None and self.last_seq is not None
        ):  # When resuming a previous WebSocket connection that was closed.
            self.send(
                {
                    "op": OPCODES.RESUME,
                    "d": {
                        "token": self.Client.token,
                        "session_id": self.session_id,  # The ID of the sessions that is being resumed.
                        "seq": self.last_seq,  # The ID of the last received payload from the server.
                    },
                }
            )  # The WebSocket resume payload.
            self.send(
                {
                    "op": OPCODES.PRESENCE_UPDATE,
                    "d": {
                        "status": self.Client.Database.Settings.get("presence")["status"],
                        "since": 0,
                        "activities": [],
                        "afk": False,
                    },
                }
            )  # The presence update payload.
        else:  # A completely new WebSocket session.
            self.send(
                {
                    "op": OPCODES.IDENTIFY,
                    "d": {
                        "token": self.Client.token,
                        "capabilities": 509,
                        "properties": {
                            "os": "windows",
                            "browser": "firefox",
                            "device": "",
                            "system_locale": self.Client.locale,
                            "browser_user_agent": self.Client.user_agent,
                            "browser_version": self.Client.user_agent.split("/")[-1],
                            "os_version": round(
                                float(
                                    self.Client.user_agent.split(" ")[3].replace(
                                        ";", ""
                                    )
                                )
                            ),
                            "referrer": "",
                            "referring_domain": "",
                            "referring_current": "",
                            "referring_domain_current": "",
                            "release_channel": "stable",
                            "client_build_number": self.Client.build_number,
                            "client_event_source": None,
                        },
                        "presence": {
                            "status": self.Client.Database.Settings.get("presence")["status"],
                            "since": 0,
                            "activities": [],
                            "afk": False,
                        },
                        "compress": False,
                        "client_state": {
                            "guild_hashes": {},
                            "highest_last_message_id": "0",
                            "read_state_version": 0,
                            "user_guild_Settings_version": -1,
                            "user_Settings_version": -1,
                        },
                    },
                }
            )  # The identify payload

        self.send(
            {
                "op": OPCODES.VOICE_STATE_UPDATE,
                "d": {
                    "guild_id": None,
                    "channel_id": None,
                    "self_mute": True,
                    "self_deaf": False,
                    "self_video": False,
                },
            }
        )  # The voice state update payload.
        
        self.last_seq = None
        self.reconnect = False
        
        self.Client.log("DEBUG", "Ready to receive commands.")

    def on_message(self, event: str) -> None:
        """Parses and handles each message sent by Discord through the gateway. It sends commands to the ‘cmd_handler’ function for more complex tasks.

        Args:
            event (str): The message received by the program.

        Returns:
            NoneType

        """

        event = self.decompress(event)  # Parse the event.
        
        self.last_seq = event[
            "s"
        ]  # Update the last sequence number received (used for reconnecting).

        if self.last_heartbeat is not None:
            self.Client.latency = f"{perf_counter() - self.last_heartbeat} ms"  # Calculate latency from subtracting the time the client sent the heartbeat from the time the server sent an acknowledgement of the heartbeat.

        if (
            event["op"] == OPCODES.HELLO
        ):  # The event sent when the client connects to the WebSocket.
            self.heartbeat_interval = (
                event["d"]["heartbeat_interval"] / 1000
            )  # Get the hearbeat interval in seconds (Discord sends it in milliseconds)

        elif (
            event["op"] == OPCODES.INVALID_SESSION
        ):  # If the WebSocket session was invalidated.
            self.reconnect = False
            self.last_seq = 0
            self.ws.close()
        elif (
            event["op"] == OPCODES.HEARTBEAT
        ):  # If the server is requesting a heartbeat.
            self.send({"op": OPCODES.HEARTBEAT, "d": self.last_seq})
        elif (
            event["op"] == OPCODES.RECONNECT
        ):  # If Discord wants the client to create a new WebSocket connection.
            self.reconnect = True
            self.ws.close()

        if (
            event["t"] == EVENTS.READY
        ):  # The event sent when the client completes the inital handshake with the gateway.
            self.session_id = event["d"]["session_id"]
        elif event["t"] == EVENTS.MESSAGE_CREATE:  # A new message is sent
            self.Client.Database.Info.set("stats.messages_received", self.Client.Database.Info.get("stats")["messages_received"] + 1)

            if event["d"]["author"]["id"] == self.Client.id:
                if (
                    event["d"]["content"][:8].lower() == "lightstart "
                    and "guild_id" in event["d"]
                ):
                    Thread(target=self.cmd_handler, args=[event]).start()

                elif event["d"]["channel_id"] in data["channels"]:
                    if data["channels"][event["d"]["channel_id"]]["messages"][
                        self.Client.token
                    ]["log"]:
                        data["channels"][event["d"]["channel_id"]]["messages"][
                            self.Client.token
                        ]["latest message"] = event[
                            "d"
                        ]  # Log the message

    def on_error(self, error: str) -> None:
        """Handles gateway errors.

        Args:
            error (str): The error.

        Returns:
            NoneType

        """

        self.Client.log("WARNING", f"A WebSocket error occured - `{error}`.")  # :-(

    def on_close(
        self, close_code: Optional[int] = None, close_msg: Optional[str] = None
    ) -> None:
        """Handles the gateway closing.

        Args:
            close_code (Optional[int]) = None: The close code.
            close_msg (Optional[str]) = None: The close message.

        Returns:
            NoneType

        """

        self.connected = False

        if close_code or close_msg:
            self.Client.log(
                "WARNING",
                f"WebSocket connection was closed. Close code: `{close_code}`, `{close_msg}`. The self-bot may be unresponsive for a few seconds until a new connection is made.",
            )

            if not (
                4000 < close_code <= 4010
            ):  # Discord requested a new WebSocket connection
                self.reconnect = True

        self.session_start()

    def cmd_handler(self, event: dict) -> Optional[bool]:
        """Handles commands and calls their relevant methods if needed.

        Args:
            event (dict): The command.

        Returns:
            Optional[bool]: Tells the program whether the command executed successfully or not.

        """

        self.Client.channel_id = event["d"]["channel_id"]
        self.Client.guild_id = event["d"]["guild_id"]
        self.Client.Database.Info.set("stats.commands_received", self.Client.Database.Info.get("stats")["commands_received"] + 1)

        if (
            self.Client.channel_id not in data["channels"]
        ):  # If a key for the command channel hasn't been made yet.
            data["channels"][self.Client.channel_id] = {
                "messages": {self.Client.token: {"log": True, "latest message": ""}}
            }  # Tells the program to start logging messages in the command channel.
        elif not data["channels"][self.Client.channel_id]["messages"][
            self.Client.token
        ][
            "log"
        ]:  # If there is already a key for the command channel.
            data["channels"][self.Client.channel_id]["messages"][
                "log"
            ] = True  # Also starts the logging of messages.

        try:
            Args = Parse_Args(event["d"]["content"])  # Parse the message.

        except Exception:
            self.Client.log(
                "WARNING",
                f"An unexpected error occured while processing the event {event['d']}: `{exc_info()}`",
            )

            self.Client.send_webhook(
                {
                    "colourless": f"An **unexpected error** occured while processing the command.\n\n**```\n{exc_info()}```**",
                    "coloured": f"An **unexpected error** occured while processing the command.\n\n**```python\n{exc_info()}```**",
                    "embed": {
                        "content": None,
                        "embeds": [
                            {
                                "title": "Error",
                                "description": f"An **unexpected error** occured while processing the command.\n\n**```python\n{exc_info()}```**",
                                "color": 16712194,
                                "footer": {
                                    "text": "Bot made by splewdge#1893 - GitHub: 'splewdge'.",
                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954?v=4",
                                },
                            }
                        ],
                        "username": "lightStart",
                        "attachments": [],
                    },
                },
            )

        data["channels"][self.Client.channel_id]["messages"] = {
            "log": False,
            "latest message": "",
        }  # Tells the program to stop logging messages in the command channel

    def decompress(self, event: str) -> dict:
        """Converts the gateway payloads into dictionaries.

        Args:
            event (str): The payload.

        Returns:
            dict: The parsed payloads

        """

        return loads(event)  # Parse the event into a dictionary

    def send(self, payload: dict) -> None:
        """Sends a payload to the gateway.

        Args:
            payload (dict): The payload.

        Returns:
            NoneType

        """

        self.ws.send(
            dumps(payload)
        )  # Convert the dictionary into a string and send it to the gateway


    def send_heartbeat(self) -> None:
        """Repeatedly sends a heartbeat to the gateway to keep the gateway from closing.

        Args:
            NONE

        Returns:
            NoneType

        """

        last_heartbeat = datetime.now()

        while True:
            while (
                not self.connected or self.heartbeat_interval is None
            ):  # If the client isn't connected to the WebSocket or the heartbeat interval hasn't been received yet.
                last_heartbeat = datetime.now()

            if (
                datetime.now() - last_heartbeat
            ).total_seconds() > self.heartbeat_interval:
                try:
                    self.send({"op": OPCODES.HEARTBEAT, "d": self.last_seq})
                    self.last_heartbeat = perf_counter()
                    last_heartbeat = datetime.now()
                except Exception:
                    pass
