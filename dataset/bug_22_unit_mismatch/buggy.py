def to_seconds(minutes):
    """Converts a duration given in minutes into seconds."""
    return minutes


def total_seconds(events):
    """Given a list of durations in minutes, returns the total in seconds."""
    total = 0
    for minutes in events:
        total += to_seconds(minutes)
    return total
