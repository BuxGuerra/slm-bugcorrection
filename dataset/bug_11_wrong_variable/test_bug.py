from solution import max_in_list


def test_max_not_last():
    assert max_in_list([3, 1, 2]) == 3


def test_max_in_middle():
    assert max_in_list([1, 5, 2]) == 5


def test_single():
    assert max_in_list([42]) == 42


def test_negatives():
    assert max_in_list([-3, -1, -7]) == -1
