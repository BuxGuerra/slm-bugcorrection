from solution import sum_range


def test_basic():
    assert sum_range(5) == 15


def test_one():
    assert sum_range(1) == 1


def test_ten():
    assert sum_range(10) == 55


def test_zero():
    assert sum_range(0) == 0
