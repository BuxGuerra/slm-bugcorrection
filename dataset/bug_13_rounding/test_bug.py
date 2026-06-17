from solution import round_price


def test_rounds_up():
    assert round_price(2.6) == 3


def test_rounds_down():
    assert round_price(2.4) == 2


def test_already_integer():
    assert round_price(5.0) == 5


def test_larger_value():
    assert round_price(3.7) == 4
