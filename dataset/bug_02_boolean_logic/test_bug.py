from solution import is_valid_age


def test_valid():
    assert is_valid_age(25) is True


def test_lower_bound():
    assert is_valid_age(0) is True


def test_upper_bound():
    assert is_valid_age(120) is True


def test_negative():
    assert is_valid_age(-5) is False


def test_too_large():
    assert is_valid_age(200) is False
