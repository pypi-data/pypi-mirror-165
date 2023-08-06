'''This module defines valuation engine components.'''
from logging import debug, warn
import time
import requests
import pandas as pd
from datetime import datetime
from frostaura.data_access import IPublicAssetDataAccess
from frostaura.data_access import IResourcesDataAccess
from frostaura.models.valuation_result import ValuationResult
from frostaura.models.symbol_data import SymbolData
from frostaura.engines.asset_valuation_engine import IAssetValuationEngine

class GrahamValuationEngine(IAssetValuationEngine):
    '''Valuation-related functionality using the discounted free cash flow method.'''
    pe_base_non_growth_company: float = 8.5
    average_yield_of_aaa_corporate_bonds: float = 4.4
    current_yield_of_aaa_corporate_bonds: float = 4.27
    margin_of_safety: float = 0.5

    def __init__(self, html_data_access: IResourcesDataAccess, public_asset_data_access: IPublicAssetDataAccess, config: dict = {}):
        self.html_data_access = html_data_access
        self.public_asset_data_access = public_asset_data_access
        self.config = config

    def __determine_intrinsic_value__(self,
                                      eps: float,
                                      pe_base_non_growth_company: float,
                                      annual_growth_projected: float,
                                      average_yield_of_aaa_corporate_bonds: float,
                                      current_yield_of_aaa_corporate_bonds: float) -> float:
        value: float = eps * (pe_base_non_growth_company + 2 * annual_growth_projected) * average_yield_of_aaa_corporate_bonds / current_yield_of_aaa_corporate_bonds

        return value

    def __determine_divident_payout_frequency_in_months__(self, symbol: str) -> int:
        try:
            epoch_now: int = int(time.time())
            url: str = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=1502928000&period2={epoch_now}&interval=1d&events=div&includeAdjustedClose=true'
            response: requests.Response = requests.get(url, headers={
                'User-Agent': 'PostmanRuntime/7.29.0'
            })
            file_name: str = f'{symbol}_dividend_history.csv'

            with open(file_name, 'wb') as f:
                f.write(response.content)

            now: datetime = datetime.now()
            start_period: datetime = datetime(year=now.year-1, month=1, day=1)
            end_period: datetime = datetime(year=now.year, month=1, day=1)
            dividend_history = pd.read_csv(file_name)
            dividend_history['Date'] = pd.to_datetime(dividend_history['Date'])
            dividends_paid_annually: int = dividend_history \
                .loc[dividend_history['Date'] >= start_period] \
                .loc[dividend_history['Date'] < end_period] \
                .shape[0]

            if dividends_paid_annually <= 0:
                return 0

            divident_payout_frequency_in_months: int = 12 / dividends_paid_annually

            return int(divident_payout_frequency_in_months)
        except Exception:
            return 0

    def valuate(self, symbol: str) -> ValuationResult:
        '''Valuate a given asset.'''

        try:
            # Get values from the config passed in if applicable otherwise fall back to defaults specified in this class.
            pe_base_non_growth_company: float = self.config['pe_base_non_growth_company'] if 'pe_base_non_growth_company' in self.config else self.pe_base_non_growth_company
            average_yield_of_aaa_corporate_bonds: float = self.config['average_yield_of_aaa_corporate_bonds'] if 'average_yield_of_aaa_corporate_bonds' in self.config else self.average_yield_of_aaa_corporate_bonds
            current_yield_of_aaa_corporate_bonds: float = self.config['current_yield_of_aaa_corporate_bonds'] if 'current_yield_of_aaa_corporate_bonds' in self.config else self.current_yield_of_aaa_corporate_bonds
            margin_of_safety: float = self.config['margin_of_safety'] if 'margin_of_safety' in self.config else self.margin_of_safety

            # Values required from a public source.
            symbol_data: SymbolData = self.public_asset_data_access.get_symbol_data(symbol=symbol)
            company_name: str = symbol_data.company_name
            annual_dividend_percentage: float = symbol_data.annual_dividend_percentage
            eps_ttm: float = symbol_data.eps_ttm
            current_price: float = symbol_data.current_price

            debug(f'EPS: {eps_ttm}')
            debug(f'pe_base_non_growth_company: {pe_base_non_growth_company}')
            debug(f'annual_growth_projected: {symbol_data.future_growth_rate*100}')
            debug(f'average_yield_of_aaa_corporate_bonds: {average_yield_of_aaa_corporate_bonds}')
            debug(f'current_yield_of_aaa_corporate_bonds: {current_yield_of_aaa_corporate_bonds}')

            intrinsic_value: float = self.__determine_intrinsic_value__(eps=eps_ttm,
                                                                        pe_base_non_growth_company=pe_base_non_growth_company,
                                                                        annual_growth_projected=symbol_data.future_growth_rate*100,
                                                                        average_yield_of_aaa_corporate_bonds=average_yield_of_aaa_corporate_bonds,
                                                                        current_yield_of_aaa_corporate_bonds=current_yield_of_aaa_corporate_bonds)

            debug(f'Intrinsic Value: $ {intrinsic_value} vs. Current Price: $ {current_price} based on the Benjamin Graham valuation method.')

            return ValuationResult(
                symbol=symbol,
                company_name=company_name,
                current_price=current_price,
                valuation_price=intrinsic_value,
                valuation_method='benjamin_graham_valuation',
                margin_of_safety=margin_of_safety,
                annual_dividend_percentage=annual_dividend_percentage,
                eps_ttm=eps_ttm,
                eps_five_years=None,
                pe_ratio=None,
                divident_payout_frequency_in_months=self.__determine_divident_payout_frequency_in_months__(symbol=symbol)
            )
        except Exception as e:
            warn(f'Error valuating symbol "{symbol}": {str(e)}')
            return None
