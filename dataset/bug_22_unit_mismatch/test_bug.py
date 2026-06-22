from solution import total_seconds


def test_single():
    assert total_seconds([1]) == 60


def test_several():
    assert total_seconds([1, 2, 3]) == 360


def test_empty():
    assert total_seconds([]) == 0


def test_with_zero():
    assert total_seconds([0, 5]) == 300
