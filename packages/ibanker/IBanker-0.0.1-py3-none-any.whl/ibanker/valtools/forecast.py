from .forecasttools import *

class Forecast:
    """
    A class for forecasting lists of numbers
    """

    def __init__(self):
        pass
    
    def forecast(self, iter: list, by=5, decimals: int = 0, factor_: float = None
):
        return forecast(iter, by, decimals, factor_)
    
    def forecasts(self, *iters: list, by: int = 5, decimals: int = 0):
        return forecasts(*iters, by, decimals)