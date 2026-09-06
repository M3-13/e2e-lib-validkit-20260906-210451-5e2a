import re
import unicodedata

_PATTERN = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("slugify() expects a str")

    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    replaced = _PATTERN.sub("-", lowered)
    return replaced.strip("-")
