from solution import safe_length


def test_string():
    assert safe_length("abc") == 3


def test_none():
    assert safe_length(None) == 0


def test_empty_string():
    assert safe_length("") == 0


def test_list():
    assert safe_length([1, 2]) == 2
