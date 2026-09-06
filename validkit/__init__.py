"""validkit - dependency-free validation and normalization helpers.

Public API: nine pure, individually usable functions, each implemented in its
own module. Import every name here so callers can do a single
``from validkit import ...`` without touching the internal modules.
"""

from validkit.accents import strip_accents
from validkit.clamp import clamp
from validkit.email import is_valid_email
from validkit.iban import is_valid_iban
from validkit.isbn import is_valid_isbn13
from validkit.luhn import luhn_check
from validkit.phone import normalize_phone
from validkit.secret import mask_secret
from validkit.slug import slugify

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "clamp",
    "is_valid_email",
    "is_valid_iban",
    "is_valid_isbn13",
    "luhn_check",
    "mask_secret",
    "normalize_phone",
    "slugify",
    "strip_accents",
]
