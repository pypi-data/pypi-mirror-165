from re import I, compile

from lightStart.utils.logger import log
from lightStart.utils.requests import Request


def get_build_number() -> str:
    req = Request(
        f"https://discord.com/app", headers={"User-Agent": "Mozilla/5.0"}
    ).content

    js_file_regex = compile(r"([a-zA-z0-9]+)\.js", I)

    asset = js_file_regex.findall(req)[-1]

    assert_file_request = Request(
        f"https://discord.com/assets/{asset}.js", headers={"User-Agent": "Mozilla/5.0"}
    ).content

    try:
        build_info_strings = (
            compile("Build Number: [0-9]+, Version Hash: [A-Za-z0-9]+")
            .findall(assert_file_request)[0]
            .replace(" ", "")
            .split(",")
        )
    except Exception:
        log("WARNING", "Failed to get latest build number. Trying again.")
        
        build_number = get_build_number()
    else:
        build_number = build_info_strings[0].split(":")[-1]

    return build_number
