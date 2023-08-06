from json import dumps, loads
from json.decoder import JSONDecodeError
from os import makedirs
from os.path import exists, isfile, splitext
from shutil import copy
from typing import Any, Optional

from lightStart.database.exceptions import (
    FileCorrupted,
    FileNotFound,
    InvalidFileType,
    KeyNotFound,
    PathNotFound,
)
from lightStart.utils.files import download
from lightStart.utils.merge import recursive_merge


class File:
    """
    Creates a `File` class for the file specified with functions for setting & getting variables.

    Attributes:
        original_path (str): The path to the file given by the user.
        path (str): The path to the file not including the file extension.
        extension (str): The file extension (including the leading full stop).
        f (io.TextIoWrapper): The file handler object.
        dict (dict): The parsed file.

    Methods:
        get(self, item: str) -> Any
        set(self, item: str, value: str) -> None
        update(self) -> None
    """

    def __init__(self, path: str) -> None:
        """
        The initializer function for the class.

        Args:
            path (str): The path of the file to open.

        Returns:
            None (NoneType)
        """

        self.original_path = path
        self.path, self.extension = splitext(path)  # Get the file path and extension.

        del path

        if not exists(self.original_path):
            raise PathNotFound(f"Path `{self.original_path}` does not exist.")
        elif not isfile(self.original_path):
            raise FileNotFound(f"Path `{self.original_path}` does not point to a file.")
        elif self.extension != ".json":  # Supports only JSON files.
            raise InvalidFileType(
                f"Expected file of type `.json`, got file of type `{self.extension}`."
            )

        try:
            self.f = open(self.original_path, "r+")
            
            self.dict = loads(self.f.read())
        except JSONDecodeError as exception:
            raise FileCorrupted(
                exception
            )  # The error will be caught in the function which called this class.

    def get(self, key: str) -> Any:
        """
        Gets the item specified by the user, or raises `database.exceptions.KeyNotFound` if the key is not found.

        Args:
            key (str): The key of the item to be found.

        Returns:
            value (typing.Any): The value of the key.
        """

        key = "".join(
            [f'["{item}"]' for item in key.split(".")]
        )  # Convert the item path into a dictionary compatible one (e.g. `settings.prefix` -> `["settings"]["prefix"]`).
        
        try:
            output = {}
            
            exec(
                f'var = self.dict{"".join(arg for arg in key)}', {**globals(), "self": self}, output
            )
            
            return output["var"]
        except KeyError:
            raise KeyNotFound(f"Key `{key}` was not found.")

    def set(self, key: str, value: Any) -> None:
        """
        Changes the value of the key specified by the user to the value specifed (by the user  ͡° ͜ʖ ͡°), or raises `database.exceptions.KeyNotFound` if the key is not found.

        Args:
            key (str): The key of the item to be changed.
            value (Any): The value to change the key to.

        Returns:
            None (NoneType)
        """

        key = "".join(
            [f'["{item}"]' for item in key.split(".")]
        )  # For an explanation, look at the first line of the `get` function in this class.

        try:
            exec(
                f'self.dict{"".join(arg for arg in key)} = {value}',
            )

            self.update()
        except KeyError:
            raise KeyNotFound(f"Key `{key}` was not found.")

    def update(self) -> None:
        self.f.seek(0)  # Move the cursor to the start of the file.

        self.f.truncate()  # Remove everything in the file after the cursor.

        self.f.write(
            dumps(self.dict, indent=4)
        )  # Convert the dictionary into a string (which is indented to make it look nice) & write it to the file.

        self.f.flush()  # Make sure the changed take effect immediately.


class Repository:
    """
    Creates a `Repository` class for the account specified with functions for creating, repairing & modifying the database files.

    Attributes:
        Client (discord.client.Instance): The account's API wrapper class.
        Database (database.core.File): The wrapper for the account's database file.
        Settings (database.core.File): The wrapper for the account's settings file.
        Info (database.core.File): The wrapper for the account's info file.

    Methods:
        create_database_file(self) -> None
        create_settings_file(self) -> None
        create_info_file(self) -> None

        def verify_database_file(
            self, database: Optional[dict] = None, database_template: Optional[dict] = None
        ) -> bool:

        def verify_settings_file(
            self, settings: Optional[dict] = None, settings_template: Optional[dict] = None
        ) -> bool:

        def verify_info_file(self) -> None:
    """

    def __init__(self, Client) -> None:
        """
        The initializer function for the class.

        Args:
            Client (discord.client.Instance): The account's API wrapper class.

        Returns:
            None (NoneType)
        """

        self.Client = Client

        del Client

        if not exists(
            f"{self.Client.cwd}database"
        ):  # Questioning why this should happen, but as a failsafe ;_)
            makedirs(f"{self.Client.cwd}database", exist_ok=True)

        if not exists(
            f"{self.Client.cwd}database/{self.Client.id}"
        ):  
            makedirs(f"{self.Client.cwd}database/{self.Client.id}", exist_ok=True)
            
            # Need to create a new database
            self.create_database_file()
            self.create_settings_file()
            self.create_info_file()

            self.Database = File(
                f"{self.Client.cwd}database/{self.Client.id}/database.json"
            )
            self.Settings = File(
                f"{self.Client.cwd}database/{self.Client.id}/settings.json"
            )
            self.Info = File(f"{self.Client.cwd}database/{self.Client.id}/info.json")
        else:
            try:
                self.Database = File(
                    f"{self.Client.cwd}database/{self.Client.id}/database.json"
                )
            except (PathNotFound, FileNotFound, FileCorrupted) as exception:
                self.Client.log(
                    "WARNING",
                    f"`database.json` file is corrupted - {exception}. Resetting to default.",
                )
                self.create_database_file()
                self.Database = File(
                    f"{self.Client.cwd}database/{self.Client.id}/database.json"
                )
            else:
                self.verify_database_file()

            try:
                self.Settings = File(
                    f"{self.Client.cwd}database/{self.Client.id}/settings.json"
                )
            except (PathNotFound, FileNotFound, FileCorrupted) as exception:
                self.Client.log(
                    "WARNING",
                    f"`settings.json` file is corrupted - {exception}. Resetting to default.",
                )
                self.create_settings_file()
                self.Settings = File(
                    f"{self.Client.cwd}database/{self.Client.id}/settings.json"
                )
            else:
                self.verify_settings_file()

            try:
                self.Info = File(
                    f"{self.Client.cwd}database/{self.Client.id}/info.json"
                )
            except (PathNotFound, FileNotFound, FileCorrupted) as exception:
                self.Client.log(
                    "WARNING",
                    f"`info.json` file is corrupted - {exception}. Resetting to default.",
                )
                self.create_info_file()
                self.Info = File(
                    f"{self.Client.cwd}database/{self.Client.id}/info.json"
                )
            else:
                self.verify_info_file()

    def create_database_file(self) -> None:
        """
        Creates the account's `database.json` file.

        Args:
            None

        Returns:
            None (NoneType)
        """

        try:
            copy(
                f"{self.Client.cwd}database/templates/database.json",
                f"{self.Client.cwd}database/{self.Client.id}",
            )
        except FileNotFoundError:
            self.download_database_template()
            self.create_database_file()

    def create_settings_file(self) -> None:
        """
        Creates the account's `settings.json` file.

        Args:
            None

        Returns:
            None (NoneType)
        """

        try:
            copy(
                f"{self.Client.cwd}database/templates/settings.json",
                f"{self.Client.cwd}database/{self.Client.id}",
            )
        except FileNotFoundError:
            self.download_settings_template()
            self.create_settings_file()

    def create_info_file(self) -> None:
        """
        Creates the account's `info.json` file.

        Args:
            None

        Returns:
            None (NoneType)
        """

        with open(f"{self.Client.cwd}database/{self.Client.id}/info.json", "w+") as f:
            f.write(
                dumps(
                    {
                        "username": self.Client.username,
                        "user": self.Client.user,
                        "discriminator": self.Client.discriminator,
                        "id": self.Client.id,
                        "stats": {
                            "commands_received": 0,
                            "messages_received": 0,
                            "messages_sent": 0,
                            "messages_deleted": 0,
                            "webhooks_sent": 0,
                            "buttons_clicked": 0,
                            "dropdowns_selected": 0,
                            "slash_commands_triggered": 0,
                            "coins_gained": 0,
                        },
                    },
                    indent=4,
                )
            )

    def verify_database_file(
        self, database: Optional[dict] = None, database_template: Optional[dict] = None
    ) -> bool:
        """
        Makes sure the account's `database.json` file is not missing any keys.

        Args:
            database: Optional[dict] = None: If this is a recursive call of the function, provides the subdict of the database.
            database_template: Optional[dict] = None: If this is a recursive call of the function, provides the subdict of the database template.

        Returns:
            boolean (bool)
        """

        if database is None and database_template is None:
            try:
                with open(
                    f"{self.Client.cwd}database/templates/database.json", "r"
                ) as database_template_file:
                    database_template = loads(database_template_file.read())
            except (FileNotFoundError, JSONDecodeError) as exception:
                self.Client.log(
                    "WARNING",
                    f"`database.json` template file is corrupted - {exception}. Re-downloading now.",
                )  # Just in case people tamper with the templates.
                database_template = self.download_database_template()

            database = self.Database.dict

        for key in database_template:
            if type(key) == dict:
                if not self.verify_database_file(database[key], database_template[key]):
                    return True
            elif key not in database:
                self.Client.log(
                    "WARNING",
                    f"`database.json` file is corrupted - key {key} is missing. Repairing the file.",
                )
                self.Database.dict = recursive_merge(database, database_template)
                self.Database.update()

                return False

    def verify_settings_file(
        self, settings: Optional[dict] = None, settings_template: Optional[dict] = None
    ) -> bool:
        """
        Makes sure the account's `settings.json` file is not missing any keys.

        Args:
            settings: Optional[dict] = None: If this is a recursive call of the function, provides the subdict of the database.
            settings_template: Optional[dict] = None: If this is a recursive call of the function, provides the subdict of the database template.

        Returns:
            boolean (bool)
        """

        if settings is None and settings_template is None:
            try:
                with open(
                    f"{self.Client.cwd}database/templates/settings.json", "r"
                ) as settings_template_file:
                    settings_template = loads(settings_template_file.read())
            except (FileNotFoundError, JSONDecodeError) as exception:
                self.Client.log(
                    "WARNING",
                    f"`settings.json` template file is corrupted - {exception}. Re-downloading now.",
                )  # Just in case people tamper with the templates.
                settings_template = self.download_settings_template()

            settings = self.Settings.dict

        for key in settings_template:
            if type(key) == dict:
                if not self.verify_settings_file(settings[key], settings_template[key]):
                    return True
            elif key not in settings:
                self.Client.log(
                    "WARNING",
                    f"`settings.json` file is corrupted - key {key} is missing. Repairing the file.",
                )
                self.Settings.dict = recursive_merge(settings, settings_template)
                self.Settings.update()

                return False

    def verify_info_file(self) -> None:
        """
        Makes sure the account's `settings.json` file is not missing any keys.

        Args:
            None

        Returns:
            None (NoneType)
        """

        info = self.Info.dict

        valid = True

        if "stats" not in info:
            valid = False
        else:
            info_stats_keys = [*info["stats"]]

            if (
                "commands_received" not in info_stats_keys
                or "messages_received" not in info_stats_keys
                or "messages_sent" not in info_stats_keys
                or "messages_deleted" not in info_stats_keys
                or "webhooks_sent" not in info_stats_keys
                or "buttons_clicked" not in info_stats_keys
                or "dropdowns_selected" not in info_stats_keys
                or "slash_commands_triggered" not in info_stats_keys
                or "coins_gained" not in info_stats_keys
            ):
                valid = False

        if not valid:
            self.Client.log(
                "WARNING", f"`info.json` file is corrupted. Repairing the file."
            )
            self.Info.dict = recursive_merge(
                info,
                {
                    "username": self.Client.username,
                    "user": self.Client.user,
                    "discriminator": self.Client.discriminator,
                    "id": self.Client.id,
                    "stats": {
                        "commands_received": 0,
                        "messages_received": 0,
                        "messages_sent": 0,
                        "messages_deleted": 0,
                        "webhooks_sent": 0,
                        "buttons_clicked": 0,
                        "dropdowns_selected": 0,
                        "slash_commands_triggered": 0,
                        "coins_gained": 0
                    },
                },
            )
            self.Info.update()

    def download_database_template(self) -> str:
        """
        Downloads the template `database.json` file.

        Args:
            None

        Returns:
            database_template (str): The downloaded database template.
        """

        return download(
            "https://raw.githubusercontent.com/splewdge/lightStart/main/src/database/templates/database.json",
            f"{self.Client.cwd}database/templates/database.json",
        )

    def download_settings_template(self) -> str:
        """
        Downloads the template `settings.json` file.

        Args:
            None

        Returns:
            settings_template (str): The downloaded settings template.
        """

        return download(
            "https://raw.githubusercontent.com/splewdge/lightStart/main/src/database/templates/settings.json",
            f"{self.Client.cwd}database/templates/settings.json",
        )
