import unicodedata


def strip_accents(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("strip_accents expects a string")

    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
