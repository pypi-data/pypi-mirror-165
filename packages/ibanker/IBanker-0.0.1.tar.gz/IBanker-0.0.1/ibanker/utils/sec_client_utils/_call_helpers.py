def _units_key(called_fact) -> str:
    """
    It takes a dictionary of the form `{'units': 'metric'}` and returns the key `'units'`

    :param called_fact: The fact that was called
    :return: The key of the first element in the dictionary.
    """
    return list(called_fact.keys())[0]
