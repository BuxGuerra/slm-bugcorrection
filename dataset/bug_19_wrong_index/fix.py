def dot_product(a, b):
    """Returns the dot product of vectors `a` and `b` (same length)."""
    total = 0
    for i in range(len(a)):
        total += a[i] * b[i]
    return total
