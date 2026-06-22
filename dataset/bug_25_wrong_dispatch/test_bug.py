import math

from solution import area


def test_square():
    assert area("square", 2) == 4


def test_square_larger():
    assert area("square", 5) == 25


def test_circle():
    assert area("circle", 1) == math.pi
