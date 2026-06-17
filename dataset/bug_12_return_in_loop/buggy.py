def has_negative(nums):
    """Returns True if any number in the list is negative, False otherwise."""
    for n in nums:
        if n < 0:
            return True
        else:
            return False
