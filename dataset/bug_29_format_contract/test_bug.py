from solution import greet_all


def test_single():
    assert greet_all([("Ada", "Lovelace")]) == ["Hello, Ada Lovelace!"]


def test_several():
    assert greet_all([("Alan", "Turing"), ("Grace", "Hopper")]) == [
        "Hello, Alan Turing!",
        "Hello, Grace Hopper!",
    ]


def test_empty():
    assert greet_all([]) == []
