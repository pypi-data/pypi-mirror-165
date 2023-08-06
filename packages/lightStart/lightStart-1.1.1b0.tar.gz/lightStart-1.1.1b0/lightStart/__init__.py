from argparse import ArgumentParser
from asyncio import run
from importlib.metadata import version
from json import dumps
from os.path import dirname
from subprocess import check_call
from sys import executable

from lightStart.main import start
from lightStart.utils.console import clear
from lightStart.utils.requests import Request


def main() -> None:
    try:
        __import__(
            "sys"
        ).frozen  # If the script is has been compiled, then the sys module with have the attribute `frozen`.
    except AttributeError:
        cwd = dirname(
            __file__
        )  # The script is not compiled, so get the cwd through the first argument passed to the python interprter.
    else:
        cwd = dirname(
            executable
        )  # The script is compiled, so get the cwd through the executable path.

    cwd = f"{cwd}\\"

    parser = ArgumentParser(
        description="A fast, free, and open-source Dank Memer self-bot."
    )

    parser.add_argument(
        "--db",
        help="If supplied, the program will print the database directory path, and exit.",
        action="store_true",
    )

    args = parser.parse_args()

    if args.db:
        try:
            with open(f"{cwd}database/credentials.json", "x") as f:
                f.write(dumps({"TOKENS": ["TOKEN_1"]}, indent=4))
        except FileExistsError:
            pass
        else:
            print(f"Made file `{cwd}database/credentials.json`.\n")
            
        exit(print(f"{cwd}database"))

    req = Request("https://pypi.org/pypi/lightstart/json")

    if not 199 < req.status_code < 300:
        return None

    latest_version, current_version = req.content["info"]["version"], version(
        "lightStart"
    )

    if latest_version != current_version:
        choice = input(
            f"Update available ({current_version} -> {latest_version}). Would you like to update (Y/n): "
        )

        if choice == "Y":
            check_call([executable, "-m", "pip", "install", "lightStart", "-U"])

            exit(__import__("lightStart").main.start())
        else:
            print("Aborting update.")

    clear()

    exit(run(start(cwd, current_version)))
