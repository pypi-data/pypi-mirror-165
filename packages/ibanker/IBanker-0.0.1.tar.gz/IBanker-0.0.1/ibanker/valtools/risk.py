from .risktools import *

class Risk:
    def __init__(self):
        self.corporate_tax_rate = get_corporate_tax_rate()
        self.market_return = get_market_return()
        self.riskless_rate = get_riskless_rate()
        self.risk_premium = get_risk_premium()
    
    def get_corporate_tax_rate(self):
        return self.corporate_tax_rate
    
    def get_market_return(self):
        return self.market_return
    
    def get_riskless_rate(self):
        return self.riskless_rate
    
    def get_risk_premium(self):
        return self.risk_premium
    
    def get_beta_(self, ticker, exchange='^gspc'):
        return get_beta(ticker, exchange)
    
    def get_capm_(self, ticker, exchange='^gspc'):
        return get_capm(ticker, exchange)
    
class TickerRisk(Risk):
    def __init__(self, ticker, exchange='^gspc'):
        super().__init__()
        self.ticker = ticker
        self.exchange = exchange
        self.beta = self.get_beta()
        self.capm = self.get_capm()
        
    def get_beta(self):
        return self.get_beta_(self.ticker, self.exchange)
        
    def get_capm(self):
        return self.get_capm_(self.ticker, self.exchange)
    
    
    
    