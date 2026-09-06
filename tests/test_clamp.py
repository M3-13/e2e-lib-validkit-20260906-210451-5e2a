import pytest

from validkit.clamp import clamp


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_range():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above_range():
    assert clamp(12, 0, 10) == 10


def test_clamp_at_lower_boundary():
    assert clamp(0, 0, 10) == 0


def test_clamp_at_upper_boundary():
    assert clamp(10, 0, 10) == 10


def test_clamp_accepts_floats():
    assert clamp(5.5, 0.0, 10.0) == 5.5
    assert clamp(-3.0, 0.0, 10.0) == 0.0
    assert clamp(12.0, 0.0, 10.0) == 10.0


def test_clamp_low_greater_than_high_raises_value_error():
    with pytest.raises(ValueError):
        clamp(1, 5, 2)


@pytest.mark.parametrize(
    "value, low, high",
    [
        (None, 0, 10),
        ("5", 0, 10),
        (5, None, 10),
        (5, 0, None),
        (5, "0", 10),
        (5, 0, "10"),
    ],
)
def test_clamp_non_numeric_raises_type_error(value, low, high):
    with pytest.raises(TypeError):
        clamp(value, low, high)


@pytest.mark.parametrize(
    "value, low, high",
    [
        (True, 0, 10),
        (5, False, 10),
        (5, 0, True),
    ],
)
def test_clamp_bool_raises_type_error(value, low, high):
    with pytest.raises(TypeError):
        clamp(value, low, high)
