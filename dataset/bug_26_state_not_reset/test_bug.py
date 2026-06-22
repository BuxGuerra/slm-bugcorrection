from solution import dedupe


def test_basic():
    assert dedupe([1, 2, 2, 3]) == [1, 2, 3]


def test_does_not_leak_between_calls():
    assert dedupe([1, 2, 3]) == [1, 2, 3]
    assert dedupe([1, 2, 3]) == [1, 2, 3]


def test_empty():
    assert dedupe([]) == []
