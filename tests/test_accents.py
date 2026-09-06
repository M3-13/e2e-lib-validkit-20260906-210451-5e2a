import pytest

from validkit.accents import strip_accents


def test_strip_accents_cafe_muenchen():
    assert strip_accents("Café München") == "Cafe Munchen"


def test_strip_accents_preserves_sharp_s():
    assert strip_accents("Straße") == "Straße"


def test_strip_accents_common_diacritics():
    assert strip_accents("áéíóú àèìòù âêîôû äëïöü") == "aeiou aeiou aeiou aeiou"


def test_strip_accents_no_diacritics_unchanged():
    assert strip_accents("hello world") == "hello world"


def test_strip_accents_empty_string():
    assert strip_accents("") == ""


def test_strip_accents_none_raises_typeerror():
    with pytest.raises(TypeError):
        strip_accents(None)


def test_strip_accents_non_string_raises_typeerror():
    with pytest.raises(TypeError):
        strip_accents(123)
