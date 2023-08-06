import numpy as np

def _basic_ratio(item1, item2, decimals=2):
    return np.around(np.divide(item1, item2), decimals)
