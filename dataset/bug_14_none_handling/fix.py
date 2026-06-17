def safe_length(s):
    """Returns the length of `s`, or 0 when `s` is None."""
    if s is None:
        return 0
    return len(s)
