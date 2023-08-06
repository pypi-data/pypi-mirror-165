from ..utils.sec_client_utils._call_helpers import _units_key
from .base import BaseClient


class Caller(BaseClient):
    def __init__(self, ticker):
        super().__init__(ticker)

    def call_fact(self, fact):
        """
        `call_fact` takes a fact as an argument and returns the value of that fact

        :param fact: The fact you want to call
        :return: The value of the fact.
        """
        try:
            called_fact = self._call_gaap()[fact]["units"]
        except KeyError:
            called_fact = self._call_dei()[fact]["units"]

        unit = _units_key(called_fact)
        return called_fact[unit]
