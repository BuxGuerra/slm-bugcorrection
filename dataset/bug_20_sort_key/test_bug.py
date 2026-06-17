from solution import sort_by_length


def test_basic():
    assert sort_by_length(["bbb", "a", "cc"]) == ["a", "cc", "bbb"]


def test_mixed_words():
    assert sort_by_length(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]


def test_empty():
    assert sort_by_length([]) == []
