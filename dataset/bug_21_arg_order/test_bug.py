from solution import net_price


def test_no_discount_no_tax():
    assert net_price(100, 0, 0) == 100


def test_discount_then_tax():
    # 100 -10% = 90, then +20% = 108
    assert net_price(100, 10, 20) == 108


def test_only_tax():
    assert net_price(100, 0, 10) == 110


def test_only_discount():
    assert net_price(200, 50, 0) == 100
