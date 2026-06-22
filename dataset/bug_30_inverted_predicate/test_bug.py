from solution import keep_valid


def test_mixed():
    assert keep_valid([1, -2, 3, None, 0]) == [1, 3, 0]


def test_all_invalid():
    assert keep_valid([-1, -2, None]) == []


def test_all_valid():
    assert keep_valid([5]) == [5]
