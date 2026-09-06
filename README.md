# validkit

validkit ist eine kleine, abhängigkeitsfreie Python-Bibliothek mit neun reinen,
einzeln nutzbaren Prüf- und Normalisierungsfunktionen. Sie validiert unter
anderem E-Mail-Adressen, Kreditkartennummern (Luhn), IBANs und ISBN-13,
normalisiert Telefonnummern und Zeichenketten (Diakritika, Slugs), maskiert
Geheimnisse und begrenzt Zahlen auf ein Intervall. Alle Funktionen sind
vollständig typannotiert und werfen bei ungültiger Eingabe klare `TypeError`/
`ValueError`.

## Tech-Stack

- **Sprache**: Python 3
- **Abhängigkeiten**: nur Standardbibliothek (`re`, `unicodedata`)
- **Tests**: pytest

## Installation

Keine externen Abhängigkeiten. Das Paket liegt direkt im Repository unter
`validkit/` und wird über `PYTHONPATH=.` importiert.

## Ausführen der Tests

```bash
python -m pytest -q
```

## Verwendung

```python
from validkit import (
    is_valid_email,
    luhn_check,
    is_valid_iban,
    is_valid_isbn13,
    normalize_phone,
    strip_accents,
    mask_secret,
    slugify,
    clamp,
)

is_valid_email("a@b.co")  # -> True
luhn_check("79927398713")  # -> True
is_valid_iban("DE89 3704 0044 0532 0130 00")  # -> True
is_valid_isbn13("978-3-16-148410-0")  # -> True
normalize_phone("030 123456", "DE")  # -> '+4930123456'
strip_accents("Café München")  # -> 'Cafe Munchen'
mask_secret("geheim123", keep=3)  # -> '*******123'
slugify("  Héllo Wörld! ")  # -> 'hello-world'
clamp(12, 0, 10)  # -> 10
```

## Funktionen

- `is_valid_email(text: str) -> bool` — prüft eine E-Mail-Adresse.
- `luhn_check(digits: str) -> bool` — prüft eine Ziffernfolge per Luhn-Algorithmus.
- `is_valid_iban(text: str) -> bool` — prüft eine IBAN per Modulo 97.
- `is_valid_isbn13(text: str) -> bool` — prüft eine ISBN-13 inklusive Prüfziffer.
- `normalize_phone(text: str, country_code: str) -> str` — normalisiert eine Telefonnummer nach E.164.
- `strip_accents(text: str) -> str` — entfernt Diakritika.
- `mask_secret(text: str, keep: int = 4) -> str` — maskiert alle Zeichen außer den letzten `keep`.
- `slugify(text: str) -> str` — erzeugt einen URL-fähigen Slug.
- `clamp(value: float, low: float, high: float) -> float` — begrenzt einen Wert auf `[low, high]`.
