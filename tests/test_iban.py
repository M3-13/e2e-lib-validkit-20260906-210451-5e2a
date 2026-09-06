import pytest

from validkit.iban import is_valid_iban


def test_valid_iban_with_spaces_is_true():
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_valid_iban_without_spaces_is_true():
    assert is_valid_iban("DE89370400440532013000") is True


def test_iban_with_wrong_check_digits_is_false():
    assert is_valid_iban("DE00 3704 0044 0532 0130 00") is False


def test_none_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_iban(None)


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_iban(12345678)


def test_too_short_is_false():
    assert is_valid_iban("DE89") is False


def test_invalid_country_code_is_false():
    assert is_valid_iban("12 89 3704 0044 0532 0130 00") is False


def test_non_digit_check_digits_is_false():
    assert is_valid_iban("DEXX 3704 0044 0532 0130 00") is False


def test_non_ascii_bban_character_is_false():
    assert is_valid_iban("DE89Ä") is False


def test_non_ascii_bban_character_is_false_full_length():
    assert is_valid_iban("DE89 3704 0044 0532 0130 Ä0") is False
