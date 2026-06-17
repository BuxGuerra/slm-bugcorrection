from solution import split_evenly


def test_with_remainder():
    assert split_evenly(10, 3) == 3


def test_exact():
    assert split_evenly(9, 3) == 3


def test_one_each():
    assert split_evenly(5, 5) == 1


def test_returns_int():
    assert isinstance(split_evenly(7, 2), int)
