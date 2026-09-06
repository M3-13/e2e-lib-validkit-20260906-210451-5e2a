import pytest

from validkit.phone import normalize_phone


def test_normalize_phone_german_number():
    assert normalize_phone("030 123456", "DE") == "+4930123456"


def test_normalize_phone_keeps_country_code_case_insensitive():
    assert normalize_phone("030 123456", "de") == "+4930123456"


def test_normalize_phone_removes_non_digits():
    assert normalize_phone("(0)30-123/456", "DE") == "+4930123456"


def test_normalize_phone_without_leading_zero():
    assert normalize_phone("123456", "DE") == "+49123456"


def test_normalize_phone_unknown_country_code():
    with pytest.raises(ValueError):
        normalize_phone("030 123456", "XX")


def test_normalize_phone_no_digits_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("  --  ", "DE")


def test_normalize_phone_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("", "DE")


@pytest.mark.parametrize("bad", [None, 123, 3.14, b"030", ["0"], {"n": "0"}])
def test_normalize_phone_text_wrong_type_raises_type_error(bad):
    with pytest.raises(TypeError):
        normalize_phone(bad, "DE")


@pytest.mark.parametrize("bad", [None, 49, b"DE", ["DE"], {"c": "DE"}])
def test_normalize_phone_country_code_wrong_type_raises_type_error(bad):
    with pytest.raises(TypeError):
        normalize_phone("030 123456", bad)
