import pytest

from validkit.email import is_valid_email


@pytest.mark.parametrize(
    "email",
    [
        "a@b.co",
        "user@example.com",
        "first.last@sub.domain.org",
        "name+tag@example.com",
    ],
)
def test_valid_emails(email):
    assert is_valid_email(email) is True


@pytest.mark.parametrize(
    "email",
    [
        "a@",
        "a b@c",
        "@example.com",
        "plainaddress",
        "a@b",
        "a@@b.co",
        "a b@c.co",
        "",
        "a@b c.co",
    ],
)
def test_invalid_emails(email):
    assert is_valid_email(email) is False


@pytest.mark.parametrize("value", [None, 123, 3.14, ["a@b.co"], b"a@b.co"])
def test_non_string_raises_type_error(value):
    with pytest.raises(TypeError):
        is_valid_email(value)


def test_type_error_message_has_no_traceback_markers():
    with pytest.raises(TypeError) as exc_info:
        is_valid_email(None)
    message = str(exc_info.value)
    assert "Traceback" not in message
    assert ".py" not in message
    assert "File" not in message
