from contextlib import suppress


def recursive_merge(dict1: dict, dict2: dict) -> dict:
    merged = dict1

    for key in dict2:
        if type(dict2[key]) == dict:
            merged[key] = recursive_merge(
                dict1[key] if key in dict1 else {}, dict2[key]
            )
        elif key not in dict1:
            merged[key] = dict2[key]

    return merged


def recursive_combine(dict1: dict, dict2: dict) -> dict:
    combined = dict1

    for key in dict2:
        if type(dict2[key]) == dict:
            combined[key] = recursive_combine(dict1[key], dict2[key])
        elif key in dict1:
            with suppress(TypeError):
                combined[key] += dict2[key]
        else:
            combined[key] = dict2[key]

    return combined
