from solution import average_of_three


def test_equal_values():
    assert average_of_three(3, 3, 3) == 3.0


def test_mixed():
    assert average_of_three(2, 4, 6) == 4.0


def test_with_zero():
    assert average_of_three(0, 0, 9) == 3.0
