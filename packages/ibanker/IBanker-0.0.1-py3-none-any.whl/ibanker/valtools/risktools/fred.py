from functools import lru_cache
import pandas as pd
import pandas_datareader as pdr


@lru_cache(maxsize=5)
def ten_yr_yield() -> pd.DataFrame:
    """
    "Get the 10 year treasury yield from the Federal Reserve Economic Data (FRED) database."

    The function name is ten_yr_yield. The function returns a pandas DataFrame. The function uses the
    pandas-datareader library to get the data from FRED
    :return: A dataframe with the 10 year yield
    """
    return pdr.get_data_fred("DGS10")


def ten_yr_yield_current() -> float:
    """
    > This function returns the current 10 year yield
    :return: The current 10 year yield
    """
    df = ten_yr_yield()
    return _get_current_of_series(df, "DGS10")


@lru_cache(maxsize=5)
def three_yr_yield() -> pd.DataFrame:
    """
    "Get the 3 month treasury yield from the Federal Reserve Economic Data (FRED) database."

    The function name is three_yr_yield. The function returns a pandas DataFrame. The function uses the
    pandas-datareader library to get the data from FRED
    :return: A dataframe with the 3 month yield
    """
    return pdr.get_data_fred("DTB3")


def three_yr_yield_current() -> float:
    """
    > This function returns the current 3 year yield
    :return: The current 3 month yield
    """
    df = three_yr_yield()
    return _get_current_of_series(df, "DTB3")


@lru_cache(maxsize=5)
def _current_of_series(series):
    return pdr.get_data_fred(series)[series][-1]


def _get_current_of_series(series_df, series_name) -> float:
    """
    > Given a dataframe and a column name, return the last value in that column

    :param series_df: the dataframe containing the series
    :param series_name: The name of the series you want to get the current value of
    :return: The last value of the series.
    """
    return series_df[series_name][-1]
