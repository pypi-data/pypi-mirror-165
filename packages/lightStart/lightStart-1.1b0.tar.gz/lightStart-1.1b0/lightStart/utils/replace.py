def replace(text: str, keys: dict) -> str:
    for key in keys:
        text = text.replace("{" + f"{key}" + "}", f"{keys[key]}")

    return text
