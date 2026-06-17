def max_in_list(nums):
    """Returns the largest value in the list `nums` (non-empty list)."""
    result = nums[0]
    for n in nums:
        if n > result:
            result = n
    return result
