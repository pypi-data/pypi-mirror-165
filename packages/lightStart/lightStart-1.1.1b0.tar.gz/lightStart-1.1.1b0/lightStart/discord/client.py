from base64 import b64encode
from copy import copy
from datetime import datetime
from random import uniform
from time import sleep, time
from typing import Optional, Union


from lightStart.utils.console import Back, Fore, Style
from lightStart.utils.requests import Request
from lightStart.utils.shared import data


class Instance(object):
    def __init__(
        self, cwd: str, account: dict, version: str, build_number: str
    ) -> None:
        self.startup_time = int(time())

        self.discriminator = int(account["discriminator"])
        self.id = account["id"]
        self.token = account["token"]
        self.user = account["user"]
        self.username = account["username"]

        del account["token"]

        self.api_version = 9
        self.build_number = build_number
        self.cwd = cwd
        self.latency = "Not measured yet"
        self.locale = account["locale"]
        self.log_file = open(
            f"{cwd}logs\\{version}\\{account['id']}\\{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
            "a",
            errors="ignore",
        )
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        self.generate_x_super_properties()

    def send_message(
        self,
        message: str,
    ) -> Optional[dict]:
        if self.Database.Settings.get("typing indicator.enabled?"):
            req = Request(
                f"https://discord.com/api/v9/channels/{self.channel_id}/typing",
                headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "json",
                    "Accept-Language": "en-GB,en;q=0.5",
                    "Alt-Used": "discord.com",
                    "Authorization": self.token,
                    "Connection": "keep-alive",
                    "Content-Length": 0,
                    "Host": "discord.com",
                    "Origin": "https://discord.com",
                    "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "TE": "trailers",
                    "User-Agent": self.user_agent,
                    "X-Debug-Options": "bugReporterEnabled",
                    "X-Discord-Locale": self.locale,
                    "X-Super-Properties": self.x_super_properties,
                },
                method="POST",
            )

            sleep(
                uniform(
                    self.Database.Settings.get("typing indicator.minimum"),
                    self.Database.Settings.get("typing indicator.maximum"),
                )
            )

        req = Request(
            f"https://discord.com/api/v{self.api_version}/channels/{self.channel_id}/messages",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "json",
                "Accept-Language": "en-GB,en;q=0.5",
                "Authorization": self.token,
                "Connection": "keep-alive",
                "Host": "discord.com",
                "Origin": "https://discord.com",
                "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers",
                "User-Agent": self.user_agent,
                "X-Debug-Options": "bugReporterEnabled",
                "X-Discord-Locale": self.locale,
                "X-Super-Properties": self.x_super_properties,
            },
            json={"content": message, "tts": False, "nonce": self.generate_nonce()},
            method="POST",
        )

        if 199 < req.status_code < 300:
            self.log(
                "DEBUG",
                f"Successfully sent message `{message}` in channel `{self.channel_id}`.",
            )
            self.Database.Info.set("stats.messages_sent", self.Database.Info.get("stats.messages_sent") + 1)
            return req.content
        else:
            if req.status_code == 429:
                self.log(
                    "WARNING",
                    f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after']} {'second' if req.content['retry_after'] == 1 else 'seconds'}.",
                )
                sleep(req.content["retry_after"])
                self.send_message(message)

            raise self.MessageSendError(
                f"Failed to send message `{message}` in channel `{self.channel_id}`. Status code: {req.status_code} (expected in-between 199 and 300)."
            )

    def retreive_message(
        self,
        check,
        old_latest_message: Optional[dict] = None,
        lower=False,
    ) -> Optional[dict]:
        time = datetime.now()
        old_latest_message = (
            copy(data["channels"][self.channel_id]["messages"]["latest message"])
            if old_latest_message is None
            else old_latest_message
        )

        while (datetime.now() - time).total_seconds() < self.Database.Settings.dict[
            "settings"
        ]["timeout"]:
            latest_message = copy(
                data["channels"][self.channel_id]["messages"]["latest message"]
            )

            if old_latest_message == latest_message:
                sleep(self.Database.Settings.dict["settings"]["timeout"] / 10)
                continue

            try:
                if check(latest_message):
                    break
            except Exception:
                pass

        if old_latest_message == latest_message:
            raise self.ResponseTimeout(
                f"Timeout exceeded for response ({self.Database.Settings.dict['settings']['timeout']} {'second' if self.Database.Settings.dict['settings']['timeout'] == 1 else 'seconds'}). Aborting command."
            )
        else:
            if lower:
                latest_message["content"] = latest_message["content"].lower()

            return latest_message

    def delete_message(self, message: Union[int, dict]) -> Optional[bool]:
        if type(message) == dict:
            message = message["id"]

        req = Request(
            f"https://discord.com/api/v{self.api_version}/channels/{self.channel_id}/messages/{message}",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "json",
                "Accept-Language": "en-GB,en;q=0.5",
                "Alt-Used": "discord.com",
                "Authorization": self.token,
                "Connection": "keep-alive",
                "Host": "discord.com",
                "Origin": "https://discord.com",
                "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": self.user_agent,
                "X-Debug-Options": "bugReporterEnabled",
                "X-Discord-Locale": self.locale,
                "X-Super-Properties": self.x_super_properties,
            },
            method="DELETE",
        )

        if 199 < req.status_code < 300:
            self.log(
                "DEBUG",
                f"Successfully deleted message `{message}` in channel `{self.channel_id}`.",
            )
            self.Database.Info.set("stats.messages_deleted", self.Database.Info.get("stats.messages_deleted") + 1)
            return True
        else:
            if req.status_code == 429:
                self.log(
                    "WARNING",
                    f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after']} {'second' if req.content['retry_after'] == 1 else 'seconds'}.",
                )
                sleep(req.content["retry_after"])
                self.delete_message(message)

            raise self.MessageDeleteError(
                f"Failed to deleted message `{message}` in channel `{self.channel_id}`. Status code: {req.status_code} (expected in-between 199 and 300)."
            )

    def send_webhook(self, payload: dict) -> Optional[dict]:
        if "webhook" in data["channels"][self.channel_id]:
            token = data["channels"][self.channel_id]["webhook"]["token"]
            channel_id = data["channels"][self.channel_id]["webhook"]["channel_id"]
        else:
            req = Request(
                f"https://discord.com/api/v{self.api_version}/channels/{self.channel_id}/webhooks",
                headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "json",
                    "Accept-Language": "en-GB,en;q=0.5",
                    "Alt-Used": "discord.com",
                    "Authorization": self.token,
                    "Connection": "keep-alive",
                    "Host": "discord.com",
                    "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "TE": "trailers",
                    "User-Agent": self.user_agent,
                    "X-Debug-Options": "bugReporterEnabled",
                    "X-Discord-Locale": self.locale,
                    "X-Super-Properties": self.x_super_properties,
                },
            )

            if not 199 < req.status_code < 300:
                self.log(
                    "WARNING",
                    f"Cannot send webhook in channel `{self.channel_id}`. Resorting to normal message.",
                )

                if self.Database.Settings.dict["messages"]["coloured?"]:
                    return self.send_message(payload["coloured"])
                else:
                    return self.send_message(payload["colourless"])

            token = None

            if len(req.content) > 0:
                for index in range(len(req.content)):
                    if "token" in req.content[index]:
                        token = req.content[index]["token"]
                        channel_id = req.content[index]["id"]
                        data["channels"][self.channel_id]["webhook"] = {
                            "token": token,
                            "channel_id": channel_id,
                        }
                        break

            if token is None:
                req = Request(
                    f"https://discord.com/api/v{self.api_version}/channels/{self.channel_id}/webhooks",
                    headers={
                        "Accept": "*/*",
                        "Accept-Encoding": "json",
                        "Accept-Language": "en-GB,en;q=0.5",
                        "Alt-Used": "discord.com",
                        "Authorization": self.token,
                        "Connection": "keep-alive",
                        "Host": "discord.com",
                        "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "TE": "trailers",
                        "User-Agent": self.user_agent,
                        "X-Debug-Options": "bugReporterEnabled",
                        "X-Discord-Locale": self.locale,
                        "X-Super-Properties": self.x_super_properties,
                    },
                    json={"name": "Captain Hook"},
                    method="POST",
                )

                token = req.content["token"]
                channel_id = req.content["id"]

                req = Request(
                    f"https://discord.com/api/v{self.api_version}/channels/{self.channel_id}/webhooks",
                    headers={
                        "Accept": "*/*",
                        "Accept-Encoding": "json",
                        "Accept-Language": "en-GB,en;q=0.5",
                        "Alt-Used": "discord.com",
                        "Authorization": self.token,
                        "Connection": "keep-alive",
                        "Host": "discord.com",
                        "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "TE": "trailers",
                        "User-Agent": self.user_agent,
                        "X-Debug-Options": "bugReporterEnabled",
                        "X-Discord-Locale": self.locale,
                        "X-Super-Properties": self.x_super_properties,
                    },
                )

        req = Request(
            f"https://discord.com/api/webhooks/{channel_id}/{token}",
            {"wait": True},
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "json",
                "Accept-Language": "en-GB,en;q=0.5",
                "Access-Control-Request-Headers": "content-type",
                "Access-Control-Request-Method": "POST",
                "Connection": "keep-alive",
                "Host": "discord.com",
                "Origin": "https://discohook.org",
                "Referer": "https://discohook.org",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "TE": "trailers",
                "User-Agent": self.user_agent,
            },
            json=payload["embed"],
            method="POST",
        )

        if 199 < req.status_code < 300:
            self.log(
                "DEBUG",
                f"Successfully sent webhook `{payload['embed']}` in channel `{self.channel_id}`.",
            )
            self.Database.Info.set("stats.webhooks_sent", self.Database.Info.get("stats.webhooks_sent") + 1)
            return req.content
        elif req.status_code == 404:
            del data["channels"][self.channel_id]["webhook"]
            self.send_webhook(payload)
        else:
            if req.status_code == 429:
                self.log(
                    "WARNING",
                    f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after'] / 1000} {'second' if req.content['retry_after'] / 1000 == 1 else 'seconds'}.",
                )
                sleep(req.content["retry_after"] / 1000)
                self.send_webhook(payload)

            raise self.WebhookSendError(
                f"Failed to send webhook `{payload['embed']}` in channel `{self.channel_id}`. Status code: {req.status_code} (expected in-between 199 and 300)."
            )

    def interact_button(
        self, message: str, custom_id: int, latest_message: dict
    ) -> Optional[bool]:
        req = Request(
            f"https://discord.com/api/v{self.api_version}/interactions",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "json",
                "Accept-Language": "en-GB,en;q=0.5",
                "Alt-Used": "discord.com",
                "Authorization": self.token,
                "Connection": "keep-alive",
                "Host": "discord.com",
                "Origin": "https://discord.com",
                "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers",
                "User-Agent": self.user_agent,
                "X-Debug-Options": "bugReporterEnabled",
                "X-Discord-Locale": self.locale,
                "X-Super-Properties": self.x_super_properties,
            },
            json={
                "application_id": "270904126974590976",
                "channel_id": self.channel_id,
                "data": {"component_type": 2, "custom_id": custom_id},
                "guild_id": self.guild_id,
                "message_flags": 0,
                "message_id": latest_message["id"],
                "nonce": self.generate_nonce(),
                "session_id": self.session_id,
                "type": 3,
            },
            method="POST",
        )

        if 199 < req.status_code < 300:
            self.log(
                "DEBUG",
                f"Successfully interacted with button `{custom_id}` in channel `{self.channel_id}`.",
            )
            self.Database.Info.set("stats.buttons_clicked", self.Database.Info.get("stats.buttons_clicked") + 1)
            return req.content
        else:
            if req.status_code == 429:
                self.log(
                    "WARNING",
                    f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after']} {'second' if req.content['retry_after'] == 1 else 'seconds'}.",
                )
                sleep(req.content["retry_after"])
                self.interact_button(message, custom_id, latest_message)

            raise self.ButtonInteractError(
                f"Failed to interact with button `{custom_id}` in channel `{self.channel_id}`. Status code: {req.status_code} (expected in-between 199 and 300)."
            )

    def log(self, level: str, text: str) -> None:
        if "Repository" in self.__dict__:
            if level == "DEBUG" and not self.Database.Settings.dict["logging"]["debug?"]:
                return
            elif (
                level == "WARNING" and not self.Database.Settings.dict["logging"]["warning?"]
            ):
                return

        time = datetime.now().strftime("[%x-%X]")

        print(
            f"{time}{f' - {Fore.Bright_Magenta}{self.username}{Style.RESET_ALL}' if self.username is not None else ''} - {Style.Italic}{Fore.Bright_Red if level == 'ERROR' else Fore.Bright_Blue if level == 'DEBUG' else Fore.Bright_Yellow}[{level}]{Style.RESET_ALL} | {text}"
        )

        self.log_file.write(
            f"{time}{f' - {self.username}' if self.username is not None else ''} - [{level}] | {text}\n"
        )
        self.log_file.flush()

        if level == "ERROR":
            input(
                f"\n{Style.Italic and Style.Faint}Press ENTER to exit the program...{Style.RESET_ALL}\n"
            )
            exit(1)

    def generate_nonce(self) -> str:
        return f"{int(f'{bin(round(time() * 1000) - 1420070400000)}0000000000000000000000', 2)}"

    def generate_x_super_properties(self) -> None:
        self.x_super_properties = b64encode(
            b'{"os":"Windows","browser":"Firefox","device":"","system_locale":"'
            + self.locale.encode("ascii")
            + b'","browser_user_agent":"'
            + self.user_agent.encode("ascii")
            + b'","browser_version":"'
            + str(self.user_agent.split("/")[-1]).encode("ascii")
            + b'","os_version":"'
            + str(round(float(self.user_agent.split(" ")[3].replace(";", "")))).encode(
                "ascii"
            )
            + b'","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":'
            + str(self.build_number).encode("ascii")
            + b',"client_event_source":null}'
        ).decode()

    class MessageSendError(Exception):
        pass

    class MessageDeleteError(Exception):
        pass

    class WebhookSendError(Exception):
        pass

    class ResponseTimeout(Exception):
        pass

    class SettingsUpdateError(Exception):
        pass

    class InvalidArguments(Exception):
        pass

    class ButtonInteratError(Exception):
        pass
