from solution import clean_names


def test_single():
    assert clean_names(["  alice "]) == ["Alice"]


def test_several():
    assert clean_names(["bOB", "  carol"]) == ["Bob", "Carol"]


def test_empty():
    assert clean_names([]) == []
