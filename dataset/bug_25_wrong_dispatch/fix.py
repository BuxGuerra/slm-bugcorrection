import math


def _circle_area(size):
    """Area of a circle of radius `size`."""
    return math.pi * size * size


def _square_area(size):
    """Area of a square of side `size`."""
    return size * size


def area(shape, size):
    """Returns the area of `shape` ('circle' or 'square') with the given size."""
    handlers = {
        "circle": _circle_area,
        "square": _square_area,
    }
    return handlers[shape](size)
