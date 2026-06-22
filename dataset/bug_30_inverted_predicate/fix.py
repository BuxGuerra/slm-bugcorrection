def is_invalid(x):
    """Returns True if x is invalid (None or negative)."""
    return x is None or x < 0


def keep_valid(items):
    """Returns only the valid items (not None and not negative)."""
    return [x for x in items if not is_invalid(x)]
