def is_odd(n):
    """Returns True if n is odd (n >= 0)."""
    if n == 0:
        return False
    return is_even(n - 1)


def is_even(n):
    """Returns True if n is even (n >= 0)."""
    if n == 0:
        return True
    return is_odd(n - 1)
