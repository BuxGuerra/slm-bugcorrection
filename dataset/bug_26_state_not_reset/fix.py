def _collect(seq):
    """Returns the elements of `seq` not already seen, preserving order."""
    seen = []
    result = []
    for x in seq:
        if x not in seen:
            seen.append(x)
            result.append(x)
    return result


def dedupe(seq):
    """Returns a list with duplicates removed, keeping first occurrence order."""
    return _collect(seq)
