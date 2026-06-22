from solution import is_even


def test_zero():
    assert is_even(0) is True


def test_even():
    assert is_even(2) is True
    assert is_even(4) is True


def test_odd():
    assert is_even(1) is False
    assert is_even(3) is False
