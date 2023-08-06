from . import zipper as z


def years(values, years) -> tuple:
    """
    It takes a list of values and a list of years, and returns a tuple of the same lists, but with the
    years list filled in with the correct years

    :param values: a list of values
    :param years: a list of years
    :return: A tuple of two lists.
    """
    unzipped = z.unzip(z.zipup(values, years))
    try:
        while z.find_str_in_iter(unzipped):
            z.fill_in_str_with_year(unzipped)
        values, years = unzipped
        return values, years
    except IndexError:
        values, years = unzipped
        return values, years
