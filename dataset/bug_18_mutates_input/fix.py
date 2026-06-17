def with_sum(nums):
    """Returns a NEW list equal to `nums` with the sum of the elements
    appended at the end. The original list must not be modified."""
    result = nums[:]
    result.append(sum(nums))
    return result
