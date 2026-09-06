import pytest

from validkit.luhn import luhn_check


def test_valid_number_returns_true():
    assert luhn_check("79927398713") is True


def test_number_with_swapped_digits_returns_false():
    assert luhn_check("79927398731") is False


def test_known_invalid_number_returns_false():
    assert luhn_check("79927398712") is False


def test_single_digit_zero_returns_true():
    assert luhn_check("0") is True


def test_non_digit_characters_raise_value_error():
    with pytest.raises(ValueError):
        luhn_check("7992739871a")


def test_spaces_raise_value_error():
    with pytest.raises(ValueError):
        luhn_check("7992 7398713")


def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("")


def test_none_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(None)


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(79927398713)
