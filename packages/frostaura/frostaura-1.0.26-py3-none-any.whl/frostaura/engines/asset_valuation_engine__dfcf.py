'''This module defines valuation engine components.'''
from logging import debug
import time
import requests
import pandas as pd
from datetime import datetime
from frostaura.data_access import IPublicAssetDataAccess
from frostaura.data_access import IResourcesDataAccess
from frostaura.models.valuation_result import ValuationResult
from frostaura.models.symbol_data import SymbolData
from frostaura.engines.asset_valuation_engine import IAssetValuationEngine

class DiscountedFutureCashFlowAssetValuationEngine(IAssetValuationEngine):
    '''Valuation-related functionality using the discounted free cash flow method.'''
    years_to_project: int = 5
    discount_rate: float = 0.1
    perpetual_growth_rate: float = 0.03
    margin_of_safety: float = 0.3

    def __init__(self, html_data_access: IResourcesDataAccess, public_asset_data_access: IPublicAssetDataAccess, config: dict = {}):
        self.html_data_access = html_data_access
        self.public_asset_data_access = public_asset_data_access
        self.config = config

    def __determine_intrinsic_value__(self,
                                      symbol_data: SymbolData,
                                      years_to_project: int,
                                      discount_rate: float,
                                      perpetual_growth_rate: float) -> float:
        assert symbol_data is not None
        assert years_to_project is not None and years_to_project > 0
        assert discount_rate is not None and discount_rate > 0
        assert perpetual_growth_rate is not None and perpetual_growth_rate > 0

        future_values: list = [ symbol_data.free_cash_flow * (1 + symbol_data.future_growth_rate) ]
        future_discount_factors: list = [ 1 + discount_rate ]

        # Calculate for all years.
        for year in range(2, years_to_project + 1):
            future_values.append(future_values[-1] * (1 + symbol_data.future_growth_rate))
            future_discount_factors.append(future_discount_factors[-1] * (1 + discount_rate))

        # Calculate for terminal values.
        future_values.append(future_values[-1] * (1 + perpetual_growth_rate) / (discount_rate - perpetual_growth_rate))
        future_discount_factors.append(future_discount_factors[-1])
        combined_present_value: float = 0

        for i in range(len(future_values)):
            combined_present_value += future_values[i] / future_discount_factors[i]
            
        print(f'Combined: {combined_present_value}')
        print(f'future_growth_rate: {symbol_data.future_growth_rate}')
        print(f'perpetual_growth_rate: {perpetual_growth_rate}')
        print(f'free_cash_flow: {symbol_data.free_cash_flow}')
        print(f'future_values: {future_values}')
        print(f'future_discount_factors: {future_discount_factors}')

        return  combined_present_value / symbol_data.shares_outstanding

    def __determine_divident_payout_frequency_in_months__(self, symbol: str) -> int:
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

    def valuate(self, symbol: str) -> ValuationResult:
        '''Valuate a given asset.'''

        # Get values from the config passed in if applicable otherwise fall back to defaults specified in this class.
        years_to_project: int = self.config['years_to_project'] if 'years_to_project' in self.config else self.years_to_project
        discount_rate: float = self.config['discount_rate'] if 'discount_rate' in self.config else self.discount_rate
        perpetual_growth_rate: float = self.config['perpetual_growth_rate'] if 'perpetual_growth_rate' in self.config else self.perpetual_growth_rate
        margin_of_safety: float = self.config['margin_of_safety'] if 'margin_of_safety' in self.config else self.margin_of_safety

        # Values required from a public source.
        symbol_data: SymbolData = self.public_asset_data_access.get_symbol_data(symbol=symbol)
        symbol_summary_url: str = f'https://finviz.com/quote.ashx?t={symbol}'
        symbol_summary_html: object = self.html_data_access.get_resource(path=symbol_summary_url)
        eps_ttm: float = float(symbol_summary_html.find(text='EPS (ttm)')
                                                            .find_next(class_='snapshot-td2')
                                                            .text)
        eps_five_years: float = float(symbol_summary_html
                                        .find(text='EPS next 5Y')
                                        .find_next(class_='snapshot-td2')
                                        .text
                                        .replace('%', '')) / 100
        pe_ratio: float = float(symbol_summary_html
                                    .find(text='P/E')
                                    .find_next(class_='snapshot-td2')
                                    .text)
        current_price: float = float(symbol_summary_html
                                        .find(text='Price')
                                        .find_next(class_='snapshot-td2')
                                        .text)
        annual_dividend_percentage: float = None
        annual_dividend_percentage_str = (symbol_summary_html
                                            .find(text='Dividend %')
                                            .find_next(class_='snapshot-td2')
                                            .text
                                            .split('%')[0])
        company_name: str = (symbol_summary_html.select_one('.fullview-title a b').text)

        if '-' not in annual_dividend_percentage_str:
            annual_dividend_percentage = float(annual_dividend_percentage_str)

        debug(f'EPS: {eps_ttm}, EPS Next 5 Years: {eps_five_years}%')
        debug(f'P/E Ratio: {pe_ratio}, Current Price: $ {current_price}')

        intrinsic_value: float = self.__determine_intrinsic_value__(symbol_data=symbol_data,
                                                                    years_to_project=years_to_project,
                                                                    discount_rate=discount_rate,
                                                                    perpetual_growth_rate=perpetual_growth_rate)

        debug(f'Intrinsic Value: $ {intrinsic_value} vs. Current Price: $ {current_price} based on the discounted future free cash flow method.')

        return ValuationResult(
            symbol=symbol,
            company_name=company_name,
            current_price=current_price,
            valuation_price=intrinsic_value,
            valuation_method='discounted_future_cash_flow_valuation',
            margin_of_safety=margin_of_safety,
            annual_dividend_percentage=annual_dividend_percentage,
            eps_ttm=eps_ttm,
            eps_five_years=eps_five_years,
            pe_ratio=pe_ratio,
            divident_payout_frequency_in_months=self.__determine_divident_payout_frequency_in_months__(symbol=symbol)
        )
