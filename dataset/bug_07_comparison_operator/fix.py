def count_passing(scores, threshold):
    """Counts how many scores are >= threshold (passing)."""
    count = 0
    for score in scores:
        if score >= threshold:
            count += 1
    return count
