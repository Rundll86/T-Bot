import unicodedata


def get_space_count(data: str) -> int:
    width = 0
    for ch in data:
        ea = unicodedata.east_asian_width(ch)
        if ea in ("W", "F"):
            width += 2
        else:
            width += 1
    return width
