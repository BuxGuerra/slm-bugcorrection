from solution import with_sum


def test_returns_correct_list():
    assert with_sum([1, 2, 3]) == [1, 2, 3, 6]


def test_does_not_mutate_input():
    original = [1, 2, 3]
    with_sum(original)
    assert original == [1, 2, 3]


def test_empty():
    assert with_sum([]) == [0]
