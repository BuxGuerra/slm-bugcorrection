from solution import running_totals


def test_appends_sum():
    assert running_totals([[1, 2], [3, 4]]) == [[1, 2, 3], [3, 4, 7]]


def test_does_not_mutate_input():
    rows = [[1, 2], [3, 4]]
    running_totals(rows)
    assert rows == [[1, 2], [3, 4]]


def test_empty():
    assert running_totals([]) == []
