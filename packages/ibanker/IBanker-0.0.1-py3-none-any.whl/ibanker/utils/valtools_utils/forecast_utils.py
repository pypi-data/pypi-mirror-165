import numpy as np
from cytoolz import itertoolz as iterz


def increment(num: int, by: int = 1) -> int:
    """
    `increment` takes in a number and an optional argument `by` and returns the sum of the two

    :param num: int - This is the first parameter, and it's a positional parameter
    :type num: int
    :param by: int = 1, defaults to 1
    :type by: int (optional)
    :return: the sum of the two numbers.
    """
    return np.add(num, by)


def increment_iter(iter: list, by: int = 1) -> list:
    """
    > It takes a list of numbers, and returns a new list of numbers, where each number is the previous
    number plus one

    :param iter: list
    :type iter: list
    :param by: The number of times to increment the iterator, defaults to 1
    :type by: int (optional)
    :return: A list of the next n numbers in the sequence.
    """
    for _ in range(by):
        last = iterz.last(iter)
        iter.extend([increment(last)])
    return iter


def pct_change(iter: list, decimals: int = 2) -> np.ndarray:
    """
    > The function takes a list of numbers and returns the percent change between each number in the
    list

    :param iter: list
    :type iter: list
    :param decimals: the number of decimal places to round to, defaults to 2
    :type decimals: int (optional)
    :return: The percent change of the values as a numpy array.
    """
    change = np.divide(np.diff(iter), iter[:-1])
    return np.around(change, decimals)


def growth_rate(iter: list, decimals: int = 2) -> float:
    """
    > It takes a list of numbers and returns the percentage change between the last two numbers

    :param iter: list
    :type iter: list
    :param decimals: The number of decimal places to round the growth rate to, defaults to 2
    :type decimals: int (optional)
    :return: The last value in the list of changes.
    """
    change = pct_change(iter, decimals)
    return iterz.last(change)


def factor(iter: list, decimals: int = 6) -> float:
    """
    > The function `factor` takes a list of numbers and returns the factor by which the list grows

    :param iter: list
    :type iter: list
    :param decimals: the number of decimal places to round to, defaults to 6
    :type decimals: int (optional)
    :return: The factor is being returned.
    """
    factor = np.add(growth_rate(iter, decimals), 1)
    return np.around(factor, decimals)
