def normalize(name):
    """Returns `name` stripped of surrounding spaces and title-cased."""
    return name.strip().title()


def clean_names(names):
    """Returns a new list with each name normalized."""
    result = []
    for name in names:
        normalize(name)
        result.append(name)
    return result
