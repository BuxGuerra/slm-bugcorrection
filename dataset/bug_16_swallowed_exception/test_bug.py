import pytest

from solution import get_value


def test_existing_key():
    assert get_value({"a": 1}, "a") == 1


def test_missing_key_raises():
    with pytest.raises(KeyError):
        get_value({"a": 1}, "missing")


def test_empty_dict_raises():
    with pytest.raises(KeyError):
        get_value({}, "x")
