from contextlib import suppress
from json import JSONDecodeError, loads
from os import makedirs, name

from aiomultiprocess import Worker

from lightStart.database.core import Repository
from lightStart.discord.build import get_build_number
from lightStart.discord.client import Instance
from lightStart.discord.gateway.session import WebSocket
from lightStart.utils.logger import log
from lightStart.utils.requests import Request


async def start(cwd: str, version: str) -> None:
    with open(f"{cwd}database\\credentials.json") as f:
        try:
            tokens = loads(f.read())["TOKENS"]

            log("DEBUG", "Parsed tokens from the `credentials.json` file.")
        except FileNotFoundError as e:
            log("ERROR", f"Cannot read `credentials.json` file - {e}. Have you run `lightstart --db` yet?")
        except JSONDecodeError as e:
            log("ERROR", f"Cannot read `credentials.json` file - {e}.")

        if len(tokens) == 0:
            log("ERROR", "Cannot run with 0 tokens.")

        build_number = get_build_number()
        
        loop_initializer = (
            None if name.lower() == "nt" else __import__("uvloop").new_event_loop
        )

        for token in tokens:
            req = Request(
                "https://discord.com/api/v9/users/@me", headers={"authorization": token}
            )

            if not 199 < req.status_code < 300:
                log("ERROR", f"Token `{token}` is invalid.")

                continue
            else:
                req.content[
                    "user"
                ] = f"{req.content['username']}#{req.content['discriminator']}"
                req.content["token"] = token

                log("DEBUG", f"Logged in successfully.", req.content['user'])

                with suppress(FileExistsError):
                    makedirs(f"{cwd}logs\\{version}\\{req.content['id']}")

                Worker(
                    target=session_start,
                    kwargs={
                        "cwd": cwd,
                        "account": req.content,
                        "version": version,
                        "build_number": build_number,
                    },
                    loop_initializer=loop_initializer,
                ).start()


async def session_start(
    cwd: str, account: dict, version: str, build_number: str
) -> None:
    Client = Instance(cwd, account, version, build_number)
    Client.Database = Repository(Client)
    WebSocket(Client)
