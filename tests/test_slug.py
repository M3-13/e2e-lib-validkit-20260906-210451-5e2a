import pytest

from validkit.slug import slugify


def test_slugify_hello_world():
    assert slugify("  Héllo Wörld! ") == "hello-world"


def test_slugify_empty_string():
    assert slugify("") == ""


def test_slugify_only_special_chars():
    assert slugify("!!! ###") == ""


def test_slugify_lowercases():
    assert slugify("HelloWorld") == "helloworld"


def test_slugify_special_characters():
    assert slugify("foo@bar#baz!") == "foo-bar-baz"


def test_slugify_control_characters():
    assert slugify("foo\tbar\nbaz") == "foo-bar-baz"


def test_slugify_unicode_outside_ascii():
    assert slugify("Ää Öö Üü") == "aa-oo-uu"


def test_slugify_removes_unicode_not_ascii_normalizable():
    assert slugify("Grüße 日本語") == "grue"


def test_slugify_removes_double_and_leading_dashes():
    assert slugify("--hello--world--") == "hello-world"


def test_slugify_numbers_preserved():
    assert slugify("abc123def") == "abc123def"


@pytest.mark.parametrize("bad", [None, 123, 4.5, b"bytes", [], {}])
def test_slugify_type_error(bad):
    with pytest.raises(TypeError):
        slugify(bad)
