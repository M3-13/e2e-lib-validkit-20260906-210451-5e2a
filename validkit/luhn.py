def luhn_check(digits: str) -> bool:
    if not isinstance(digits, str):
        raise TypeError("luhn_check expects a string of digits")

    if not digits:
        raise ValueError("luhn_check requires at least one digit")

    if not digits.isdigit():
        raise ValueError("luhn_check requires a string containing only digits")

    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0
