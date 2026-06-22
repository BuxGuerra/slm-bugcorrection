def bounds(page, size):
    """Returns the (start, end) slice indices for a 1-based `page` of `size` items."""
    start = (page - 1) * size
    end = start + size - 1
    return start, end


def paginate(items, page, size):
    """Returns the items on the 1-based `page`, with `size` items per page."""
    start, end = bounds(page, size)
    return items[start:end]
