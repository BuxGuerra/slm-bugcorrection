from solution import remove_last_char


def test_word():
    assert remove_last_char("hello") == "hell"


def test_single_char():
    assert remove_last_char("a") == ""


def test_trailing_newline():
    assert remove_last_char("line\n") == "line"
