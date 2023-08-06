import datetime as dt


def current_year() -> dt.datetime.year:
    """
    `current_year()` returns the current year
    :return: The current year.
    """
    return dt.datetime.now().year
