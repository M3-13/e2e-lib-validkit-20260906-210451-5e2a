import pytest

from validkit.isbn import is_valid_isbn13


def test_valid_isbn13():
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_isbn13_with_wrong_check_digit():
    assert is_valid_isbn13("978-3-16-148410-1") is False


def test_isbn13_with_wrong_length():
    assert is_valid_isbn13("978-3-16-148410") is False


def test_isbn13_none_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(None)


def test_isbn13_non_string_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(9783161484100)


def test_isbn13_with_spaces_is_valid():
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_isbn13_with_non_digit_characters_is_invalid():
    assert is_valid_isbn13("978-3-16-14841X-0") is False
