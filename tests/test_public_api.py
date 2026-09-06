import importlib

import validkit


def test_all_public_names_import_without_error():
    names = [
        "is_valid_email",
        "luhn_check",
        "is_valid_iban",
        "is_valid_isbn13",
        "normalize_phone",
        "strip_accents",
        "mask_secret",
        "slugify",
        "clamp",
    ]
    for name in names:
        assert hasattr(validkit, name), f"{name} not exported by validkit"


def test_public_names_are_callable():
    names = [
        "is_valid_email",
        "luhn_check",
        "is_valid_iban",
        "is_valid_isbn13",
        "normalize_phone",
        "strip_accents",
        "mask_secret",
        "slugify",
        "clamp",
    ]
    for name in names:
        assert callable(getattr(validkit, name)), f"{name} is not callable"


def test_version_is_defined():
    assert validkit.__version__ == "0.1.0"


def test_each_name_imports_from_its_own_module():
    module_map = {
        "is_valid_email": "validkit.email",
        "luhn_check": "validkit.luhn",
        "is_valid_iban": "validkit.iban",
        "is_valid_isbn13": "validkit.isbn",
        "normalize_phone": "validkit.phone",
        "strip_accents": "validkit.accents",
        "mask_secret": "validkit.secret",
        "slugify": "validkit.slug",
        "clamp": "validkit.clamp",
    }
    for name, module in module_map.items():
        mod = importlib.import_module(module)
        assert callable(getattr(mod, name)), f"{module}.{name} is not callable"
