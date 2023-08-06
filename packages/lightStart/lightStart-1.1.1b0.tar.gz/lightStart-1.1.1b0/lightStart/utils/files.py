from os import makedirs
from os.path import splitext

from lightStart.utils.requests import Request


class FileDownloadFailure(Exception):
    pass


def download(url: str, path: str) -> str:
    """
    Downloads the file specified to the path specified.

    Args:
        url (str): The URL of the file to download.
        path (str): The path to download the file to.

    Returns:
        file (str): The contents of the downloaded file.
    """

    makedirs(splitext(path)[0])

    req = Request(url)

    if not 199 < req.status_code < 300:
        raise FileDownloadFailure(
            f"Status code: {req.status_code} (expected in-between 199 and 300)."
        )

    with open(path, "w") as f:
        f.write(req.content)

    return req.content
