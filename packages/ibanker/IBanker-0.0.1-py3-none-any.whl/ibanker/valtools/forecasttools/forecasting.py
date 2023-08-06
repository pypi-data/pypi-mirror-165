import numpy as np
from cytoolz import itertoolz as iterz
from ...utils.valtools_utils import forecast_utils as futil
    
    
def forecast(iter: list, by=5, decimals: int = 0, factor_: float = None
) -> np.ndarray:
    """
    > The function takes a list of numbers, and returns a list of numbers that are the product of the
    last number in the list and a factor

    :param iter: list
    :type iter: list
    :param by: The number of iterations to forecast, defaults to 5 (optional)
    :param decimals: the number of decimal places to round the forecast to, defaults to 0
    :type decimals: int (optional)
    :param factor_: The factor to multiply the last value by. If None, it will be calculated
    :type factor_: float
    :return: The forecast function returns a numpy array of the forecasted values.
    """
    f = factor_ if factor_ is not None else futil.factor(iter)
    i = 0
    while i < by:
        last = iterz.last(iter)
        iter.extend([np.multiply(last, f)])
        i += 1
    return np.around(iter, decimals)

def forecasts(*iters: list, by: int = 5, decimals: int = 0) -> list:
    """
    It takes a list of iterables and returns a list of forecasts

    :param : * `iters`: a list of iterables to be forecasted
    :type : list
    :param by: The number of periods to forecast, defaults to 5
    :type by: int (optional)
    :param decimals: the number of decimal places to round the forecast to, defaults to 0
    :type decimals: int (optional)
    :return: A list of lists.
    """
    f = futil.factor(iterz.first(iters))
    return [self.forecast(iter, by, decimals, factor_=f) for iter in iters]