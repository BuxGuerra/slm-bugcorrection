def format_name(first, last):
    """Returns the full name in 'First Last' order."""
    return f"{first} {last}"


def greet_all(people):
    """Given a list of (first, last) tuples, returns 'Hello, First Last!' for each."""
    greetings = []
    for first, last in people:
        greetings.append(f"Hello, {format_name(first, last)}!")
    return greetings
