def unique(lst):
    """Returns the elements of `lst` without duplicates, preserving the order
    of first occurrence."""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
