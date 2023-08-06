import pandas as pd
from ..utils.sec_client_utils import current_year
from .dumper import dump_fact
from .loader import load_fact, load_facts
from .formatter import Formatter

formatter = Formatter()


class SECClient:
    def __init__(self):
        pass

    def get_fact(
        self,
        ticker: str,
        tag: str,
        form: str = "10-K",
        start: int = 0,
        end: int = current_year(),
    ) -> pd.DataFrame:
        """
        > This function returns a dataframe of the fact tag for the given ticker, form, start, and end

        :param ticker: The ticker symbol of the company you want to get data for
        :type ticker: str
        :param tag: The tag you want to get
        :type tag: str
        :param form: The form type. This is the form type that the SEC uses to categorize filings. The most
        common form types are 10-K and 10-Q, defaults to 10-K
        :type form: str (optional)
        :param start: The start year of the data you want, defaults to 0
        :type start: int (optional)
        :param end: The year to end the search for the fact
        :type end: int
        :return: A dataframe with the ticker as the index and the fact as the column.
        """
        fact = self._get_fact(ticker, tag, form, start, end)
        return fact.to_frame().swapaxes("index", "columns")

    def get_facts(self, ticker: str) -> pd.DataFrame:
        """
        > The function `get_facts` takes a ticker as input and returns a pandas dataframe of the facts for
        that ticker

        :param ticker: The ticker of the stock you want to get the facts for
        :type ticker: str
        :return: A dataframe of the facts for the ticker
        """
        return pd.DataFrame(load_facts(ticker))

    def _get_fact(
        self,
        ticker: str,
        tag: str,
        form: str = "10-K",
        start: int = 0,
        end: int = current_year(),
    ) -> pd.Series:
        """
        It tries to load a fact from the cache, and if it fails, it downloads the fact and tries again

        :param ticker: The ticker of the company you want to get data for
        :type ticker: str
        :param tag: The tag of the fact you want to get
        :type tag: str
        :param form: The form of the financial statement, defaults to 10-K
        :type form: str (optional)
        :param start: int = 0,, defaults to 0
        :type start: int (optional)
        :param end: The year to end the search for the fact
        :type end: int
        :return: A pandas series
        """
        try:
            fact = load_fact(ticker, tag, form, start, end)
        except ValueError:
            dump_fact(ticker, tag, form)
            return self._get_fact(ticker, tag, start, end)

        if isinstance(fact, dict):
            return formatter.format_fact(fact, tag)
