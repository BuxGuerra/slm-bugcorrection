from solution import has_negative


def test_negative_after_positives():
    assert has_negative([1, 2, -3]) is True


def test_all_positive():
    assert has_negative([1, 2, 3]) is False


def test_first_negative():
    assert has_negative([-1]) is True


def test_empty():
    assert has_negative([]) is False
