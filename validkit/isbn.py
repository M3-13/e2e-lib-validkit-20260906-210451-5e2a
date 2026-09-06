import re


def is_valid_isbn13(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("is_valid_isbn13 expects a str")

    digits = re.sub(r"[- ]", "", text)
    if not re.fullmatch(r"\d{13}", digits):
        return False

    total = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(digits))
    return total % 10 == 0
