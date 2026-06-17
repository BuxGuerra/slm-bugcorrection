from solution import sum_str_numbers


def test_basic():
    assert sum_str_numbers(["1", "2", "3"]) == 6


def test_two():
    assert sum_str_numbers(["10", "20"]) == 30


def test_empty():
    assert sum_str_numbers([]) == 0


def test_result_is_int():
    assert sum_str_numbers(["5", "5"]) == 10
