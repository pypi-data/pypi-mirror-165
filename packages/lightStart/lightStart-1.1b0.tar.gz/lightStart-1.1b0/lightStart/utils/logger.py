from datetime import datetime
from typing import Optional

from lightStart.utils.console import Fore, Style


def log(level: str, text: str, username: Optional[str] = None) -> None:
    time = datetime.now().strftime("[%x-%X]")

    print(
        f"{time}{f' - {Fore.Bright_Magenta}{username}{Style.RESET_ALL}' if username is not None else ''} - {Style.Italic}{Fore.Bright_Red if level == 'ERROR' else Fore.Bright_Blue if level == 'DEBUG' else Fore.Bright_Yellow}[{level}]{Style.RESET_ALL} | {text}"
    )

    if level == "ERROR":
        input(
            f"\n{Style.Italic and Style.Faint}Press ENTER to exit the program...{Style.RESET_ALL}\n"
        )

        exit(1)
