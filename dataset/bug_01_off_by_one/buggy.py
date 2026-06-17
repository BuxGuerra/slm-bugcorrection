def sum_range(n):
    """Sums all integers from 1 to n (inclusive)."""
    total = 0
    for i in range(1, n):
        total += i
    return total
