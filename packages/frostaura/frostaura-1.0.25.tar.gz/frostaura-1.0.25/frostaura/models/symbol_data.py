'''This module definessymbol data model components.'''

class SymbolData:
    '''A model with all the detailed information for a symbol.'''

    def __init__(self, symbol: str, future_growth_rate: float, free_cash_flow: float, shares_outstanding: float):
        self.symbol = symbol
        self.future_growth_rate = future_growth_rate
        self.free_cash_flow = free_cash_flow
        self.shares_outstanding = shares_outstanding
