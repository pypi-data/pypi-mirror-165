import matplotlib.pyplot as plt
from ..risktools import get_beta, get_capm, get_riskless_rate, get_market_return


def _interval_plot(*coords):
    return plt.plot(coords)

def _get_coords(ticker, exchange='^gspc'):
    beta = get_beta(ticker)
    capm = get_capm(ticker, exchange)
    return beta, capm

def plot_capm(ticker):
    riskless = get_riskless_rate()
    market = get_market_return()
    x, y = _get_coords(ticker)
    
    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    ax.plot([0, 1], [riskless, market])
    ax.plot([x], [y], label=ticker)
    return fig, ax