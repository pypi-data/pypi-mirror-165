'''This module defines valuation engine components.'''
from logging import debug
import time
import requests
import pandas as pd
from datetime import datetime
from frostaura.data_access import IResourcesDataAccess
from frostaura.models.valuation_result import ValuationResult
from frostaura.engines.asset_valuation_engine import IAssetValuationEngine

class FinvizAssetValuationEngine(IAssetValuationEngine):
    '''Valuation-related functionality using Finviz under-the-hood.'''

    def __init__(self, html_data_access: IResourcesDataAccess, config: dict = {}):
        self.html_data_access = html_data_access
        self.config = config

    def __determine_intrinsic_value__(self,
                                      eps_ttm: float, # Total trailing annual earnings per share.
                                      growth_rate: float, # Projected 5 year EPS.
                                      pe_ratio: float, # Price per earnings growth rate. 2x growth_rate if unsure.
                                      min_rate_of_return: float = 0.15 # Rate of return we want to make.
                              ) -> float:
        assert eps_ttm > 1
        assert growth_rate > 0 and growth_rate < 1
        assert pe_ratio > 1
        assert min_rate_of_return > 0 and min_rate_of_return < 1

        target_ten_year_eps: float = eps_ttm

        for year in range(2, 11):
            target_ten_year_eps *= (1 + growth_rate)

        target_ten_year_share_price: float = target_ten_year_eps * pe_ratio
        target_share_price: float = target_ten_year_share_price

        for year in range(2, 11):
            target_share_price /= (1 + growth_rate)

        return target_share_price

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

        intrinsic_value: float = self.__determine_intrinsic_value__(eps_ttm=eps_ttm,
                            growth_rate=eps_five_years,
                            pe_ratio=pe_ratio)

        debug(f'Intrinsic Value: $ {intrinsic_value} vs. Current Price: $ {current_price}')

        return ValuationResult(
            symbol=symbol,
            company_name=company_name,
            current_price=current_price,
            valuation_method='rain_valuation',
            margin_of_safety=0.3,
            valuation_price=intrinsic_value,
            annual_dividend_percentage=annual_dividend_percentage,
            eps_ttm=eps_ttm,
            eps_five_years=eps_five_years,
            pe_ratio=pe_ratio,
            divident_payout_frequency_in_months=self.__determine_divident_payout_frequency_in_months__(symbol=symbol)
        )
