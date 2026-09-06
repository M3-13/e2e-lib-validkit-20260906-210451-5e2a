import pytest

from validkit.secret import mask_secret


def test_masks_all_but_last_keep_chars():
    assert mask_secret("geheim123", keep=3) == "******123"


def test_text_shorter_than_default_keep_is_fully_masked():
    assert mask_secret("abc") == "***"


def test_keep_equal_to_length_is_fully_masked():
    assert mask_secret("abcd", keep=4) == "****"


def test_keep_larger_than_length_is_fully_masked():
    assert mask_secret("ab", keep=10) == "**"


def test_keep_zero_masks_everything():
    assert mask_secret("abc", keep=0) == "***"


def test_negative_keep_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("abc", keep=-1)


def test_non_string_text_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret(None)
    with pytest.raises(TypeError):
        mask_secret(123)


def test_non_int_keep_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret("abc", keep="3")
