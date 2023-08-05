'''This module defines valuation model components.'''

class ValuationResult:
    '''A model with all the post-valuation data for an asset.'''

    def __init__(self,
                 symbol: str,
                 company_name: str,
                 current_price: float,
                 valuation_method: str,
                 valuation_price: float,
                 margin_of_safety: float,
                 annual_dividend_percentage: float,
                 eps_ttm: float,
                 eps_five_years: float,
                 pe_ratio: float,
                 divident_payout_frequency_in_months: int):
        assert margin_of_safety > 0 and margin_of_safety < 1

        self.symbol = symbol
        self.company_name = company_name
        self.current_price = current_price
        self.valuation_method = valuation_method
        self.valuation_price = valuation_price
        self.fair_price = valuation_price * (1 - margin_of_safety)
        self.absolute_current_v_valuation_delta = 1 - (min(self.fair_price, current_price) / max(self.fair_price, current_price))
        self.is_overvalued = self.fair_price < current_price
        self.annual_dividend_percentage = annual_dividend_percentage
        self.eps_ttm = eps_ttm
        self.eps_five_years = eps_five_years
        self.pe_ratio = pe_ratio
        self.divident_payout_frequency_in_months = divident_payout_frequency_in_months
