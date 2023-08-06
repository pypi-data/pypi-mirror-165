'''This module definessymbol data model components.'''

class SymbolData:
    '''A model with all the detailed information for a symbol.'''

    def __init__(self,
                 symbol: str,
                 future_growth_rate: float,
                 free_cash_flow: float,
                 shares_outstanding: float,
                 company_name: str,
                 annual_dividend_percentage: float,
                 eps_ttm: float,
                 current_price: float,
                 pe_ratio: float):
        self.symbol = symbol
        self.future_growth_rate = future_growth_rate
        self.free_cash_flow = free_cash_flow
        self.shares_outstanding = shares_outstanding
        self.company_name = company_name
        self.annual_dividend_percentage = annual_dividend_percentage
        self.eps_ttm = eps_ttm
        self.current_price = current_price
        self.pe_ratio = pe_ratio
