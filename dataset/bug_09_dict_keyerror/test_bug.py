from solution import get_count


def test_existing_key():
    assert get_count({"a": 1, "b": 2}, "a") == 1


def test_missing_key():
    assert get_count({"a": 1}, "z") == 0


def test_empty_dict():
    assert get_count({}, "x") == 0
