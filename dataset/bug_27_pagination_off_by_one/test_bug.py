from solution import paginate


def test_first_page():
    assert paginate([1, 2, 3, 4, 5], 1, 2) == [1, 2]


def test_second_page():
    assert paginate([1, 2, 3, 4, 5], 2, 2) == [3, 4]


def test_page_size_three():
    assert paginate([1, 2, 3, 4, 5], 1, 3) == [1, 2, 3]


def test_last_partial_page():
    assert paginate([1, 2, 3, 4, 5], 3, 2) == [5]
