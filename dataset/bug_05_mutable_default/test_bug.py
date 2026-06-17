from solution import append_item


def test_independent_calls():
    assert append_item(1) == [1]
    assert append_item(2) == [2]
    assert append_item(3) == [3]


def test_explicit_acc():
    assert append_item(2, [1]) == [1, 2]
