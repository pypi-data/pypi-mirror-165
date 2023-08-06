import numpy as np


def nodupes(iterable) -> list:
    """
    It takes an iterable, converts it to a numpy array, removes duplicates, and returns a list

    :param iterable: any iterable (list, string, dictionary etc.)
    :return: A list of unique values from the iterable.
    """
    return np.unique(iterable).tolist()
