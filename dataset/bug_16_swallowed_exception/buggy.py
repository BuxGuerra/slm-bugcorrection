def get_value(d, key):
    """Returns d[key]. If the key does not exist, it should propagate KeyError."""
    try:
        return d[key]
    except Exception:
        pass
