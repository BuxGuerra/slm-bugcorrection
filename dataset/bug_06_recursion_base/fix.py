def factorial(n):
    """Returns n! (factorial of n), for n >= 0."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
