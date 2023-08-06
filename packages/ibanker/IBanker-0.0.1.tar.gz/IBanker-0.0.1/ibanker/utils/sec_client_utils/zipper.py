import itertools
import numpy as np


def zipup(values, years) -> list:
    """
    "zip up the values and years, reversing them first, and then reversing the result."

    The first line reverses the values. The second line reverses the years. The third line zips up the
    values and years, filling in any missing values with a dash. The fourth line reverses the zipped
    list

    :param values: a list of values
    :param years: a list of years, in chronological order
    :return: A list of tuples.
    """
    values = reversed(values)
    years = reversed(years)
    zipped = itertools.zip_longest(values, years, fillvalue="-")
    return list(reversed(list(zipped)))


def unzip(zipped) -> list:
    """
    It takes a list of tuples and returns a list of lists

    :param zipped: a list of tuples
    :return: A list of lists.
    """
    unzipped_object = zip(*zipped)
    return [list(tup) for tup in list(unzipped_object)]


def zip_unzipped(unzipped) -> list:
    """
    It takes a list of tuples, and returns a list of tuples

    :param unzipped: a tuple of two lists, the first being the values and the second being the years
    :return: A list of tuples.
    """
    values, years = unzipped
    return list(zip(values, years))


def get_str_index(unzipped) -> "index":
    """
    If the string "-" is found in the second element of the unzipped list, return the index of the last
    occurrence of "-" in the second element of the unzipped list

    :param unzipped: a tuple of two lists, the first being the list of the values of the column, the
    second being the list of the indices of the column
    :return: The index of the first string in the list.
    """
    if find_str_in_iter(unzipped):
        return np.subtract(
            len(unzipped[1]), np.subtract(unzipped[1][::-1].index("-"), 1)
        )


def find_str_in_iter(unzipped):
    """
    It returns True if the second element of the tuple contains a dash

    :param unzipped: a tuple of (key, value) pairs
    :return: A boolean value.
    """
    return "-" in unzipped[1]


def get_int_after_str(unzipped):
    """
    If there is a string in the unzipped list, return the integer that comes after it.

    :param unzipped: a list of tuples, where each tuple is a list of strings and a list of integers
    :return: The integer after the string.
    """
    if find_str_in_iter(unzipped):
        non_int_index = get_str_index(unzipped)
        int_index = non_int_index + 1
        return unzipped[1][int_index]


def fill_in_str_with_year(unzipped):
    """
    If the string 'year' is found in the unzipped list, then the year is found and the year is
    subtracted by 1. The index of the string 'year' is found and the year is inserted into the list.

    :param unzipped: a list of lists, where each list is a row of the dataframe
    """
    if find_str_in_iter(unzipped):
        year = get_int_after_str(unzipped)
        fill_in_year = year - 1
        non_int_index = get_str_index(unzipped)
        unzipped[1][non_int_index] = fill_in_year


def grouper(n, iterable):
    """
    It takes an iterable and returns an iterable of lists of length n

    :param n: the number of items to group together
    :param iterable: the iterable to be split into chunks
    :return: A list of lists, where each list is n elements long.
    """
    iterable = iter(iterable)
    return iter(lambda: list(itertools.islice(iterable, n)), [])
