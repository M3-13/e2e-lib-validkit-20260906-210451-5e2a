import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("email must be a string")

    return bool(_EMAIL_RE.match(text))
