import re

_COUNTRY_CODE = re.compile(r"^[A-Z]{2}$")


def is_valid_iban(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("iban must be a string")

    normalized = text.replace(" ", "").upper()

    if len(normalized) < 5:
        return False

    country = normalized[:2]
    check_digits = normalized[2:4]
    bban = normalized[4:]

    if not _COUNTRY_CODE.match(country):
        return False

    if not check_digits.isdigit():
        return False

    if not bban or not all(c.isascii() and c.isalnum() for c in bban):
        return False

    rearranged = bban + country + check_digits

    digits = ""
    for char in rearranged:
        if "A" <= char <= "Z":
            digits += str(ord(char) - ord("A") + 10)
        else:
            digits += char

    return int(digits) % 97 == 1
