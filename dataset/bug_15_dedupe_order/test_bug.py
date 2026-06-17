from solution import unique


def test_preserves_order():
    assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_strings_order():
    assert unique(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_no_duplicates():
    assert unique([5, 4, 6]) == [5, 4, 6]


def test_empty():
    assert unique([]) == []
