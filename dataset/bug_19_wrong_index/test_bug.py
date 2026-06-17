from solution import dot_product


def test_basic():
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32


def test_two_elements():
    assert dot_product([1, 1], [2, 3]) == 5


def test_with_zero():
    assert dot_product([0, 2], [5, 5]) == 10
