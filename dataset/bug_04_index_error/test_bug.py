from solution import get_last


def test_multiple():
    assert get_last([1, 2, 3]) == 3


def test_single():
    assert get_last([5]) == 5


def test_strings():
    assert get_last(["a", "b", "c"]) == "c"
