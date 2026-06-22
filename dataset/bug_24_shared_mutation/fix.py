def append_total(row):
    """Returns a new row equal to `row` with the sum of its values appended."""
    return row + [sum(row)]


def running_totals(rows):
    """Returns a new list of rows, each with its sum appended at the end.

    The input rows must not be modified.
    """
    return [append_total(row) for row in rows]
