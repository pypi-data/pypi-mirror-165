import yfinance as yf
import pandas as pd
import numpy as np


class Statements(yf.Ticker):
    def __init__(self, ticker, income_statement: pd.DataFrame = 'yf', balance_sheet: pd.DataFrame = 'yf'):
        super().__init__(ticker)

        if income_statement == 'yf':
            income_statement = self.financials

        self.income_statement = income_statement

        self.research_development = self.financials.loc['Research Development']
        self.income_before_taxes = self.financials.loc['Income Before Tax']
        self.net_income = self.financials.loc['Net Income']
        self.sga = self.financials.loc['Selling General Administrative']
        self.gross_progit = self.financials.loc['Gross Profit']
        self.operating_income = self.financials.loc['Operating Income']
        self.ebit = self.operating_income
        self.interest_expense = self.financials.loc['Interest Expense']
        self.income_tax_expense = self.financials.loc['Income Tax Expense']
        self.revenue = self.financials.loc['Total Revenue']
        self.operating_expenses = self.financials.loc['Total Operating Expenses']
        self.cogs = self.financials.loc['Cost Of Revenue']
        
        if balance_sheet == 'yf':
            balance_sheet = self.balance_sheet

        self.balance_sheet_ = balance_sheet
        
        self.total_liabilities = self.balance_sheet_.loc['Total Liab']
        
        self.total_stock_eq = self.balance_sheet_.loc['Total Stockholder Equity']