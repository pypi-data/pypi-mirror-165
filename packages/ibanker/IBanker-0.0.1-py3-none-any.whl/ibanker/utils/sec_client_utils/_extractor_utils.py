import datetime as dt


def _replace_string_in_period(period: str):
    """
    It takes a string, and if it's a quarter, it returns the quarter number. If it's not a quarter, it
    returns None

    :param period: The period of the data. This can be a quarter or a year
    :type period: str
    :return: A list of dictionaries.
    """
    try:
        period = int(period.replace("Q", ""))
    except ValueError:
        period = None

    return period


def _make_into_date(date_string: str) -> dt.datetime:
    """
    It takes a string in the format YYYY-MM-DD and returns a datetime object

    :param date_string: The date string to be converted into a date object
    :type date_string: str
    :return: A datetime object
    """
    year, month, day = list(map(int, date_string.split("-")))
    return dt.date(year, month, day)
