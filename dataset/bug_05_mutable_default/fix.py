def append_item(item, acc=None):
    """Returns a new list containing only `item`.

    Each call should be independent of the previous ones.
    """
    if acc is None:
        acc = []
    acc.append(item)
    return acc
