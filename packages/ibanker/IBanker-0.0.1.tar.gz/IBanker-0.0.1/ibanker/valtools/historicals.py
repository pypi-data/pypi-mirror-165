from .histtools import *

class Historicals:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.history = get_history(ticker)
        self.close = get_close(ticker)
        self.returns = get_returns(ticker)
        
    def get_history(self):
        return self.history
    
    def get_close(self):
        return self.close
    
    def get_returns(self):
        return self.returns