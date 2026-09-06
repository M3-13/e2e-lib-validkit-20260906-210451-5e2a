_COUNTRY_CODES = {
    "DE": "49",
    "AT": "43",
    "CH": "41",
}


def normalize_phone(text: str, country_code: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(country_code, str):
        raise TypeError("country_code must be a string")

    dialing_code = _COUNTRY_CODES.get(country_code.upper())
    if dialing_code is None:
        raise ValueError(f"unknown country_code: {country_code}")

    digits = "".join(ch for ch in text if ch.isdigit())
    if not digits:
        raise ValueError("phone number contains no usable digits")

    digits = digits.lstrip("0")
    if not digits:
        raise ValueError("phone number contains no usable digits")

    return "+" + dialing_code + digits
