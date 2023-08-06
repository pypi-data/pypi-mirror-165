'''This module defines Yahoo Finance data access components.'''
import yfinance as yf
import pandas as pd
from logging import info, warning
from expiringdict import ExpiringDict
from frostaura.data_access.public_asset_data_access import IPublicAssetDataAccess
from frostaura.models.symbol_data import SymbolData

class YahooFinanceDataAccess(IPublicAssetDataAccess):
    '''Yahoo Finance public asset-related functionality.'''

    def __init__(self, config: dict = {}):
        self.config = config
        self.__cache__ = ExpiringDict(max_len=999999,
                                      max_age_seconds=60*5)

    def get_symbol_history(self, symbol: str, ignore_cache: bool = False) -> pd.DataFrame:
        '''Get historical price movements for a given symbol.'''

        info(f'Fetching historical price movements for symbol "{symbol}".')

        cache_key: str = f'{symbol}-history'
        value: pd.DataFrame = self.__cache__.get(cache_key)

        if value is None or ignore_cache:
            warning(f'No item with the key "{cache_key}" existed in the cache.')
            ticker = yf.Ticker(symbol)
            value = ticker.history(period='max')
            self.__cache__[cache_key] = value
        else:
            info(f'Item for key "{cache_key}" retrieved from cache with value: {value}')

        return value

    def get_symbol_data(self, symbol: str, ignore_cache: bool = False) -> SymbolData:
        '''Get detailed information about a given symbol.'''

        info(f'Fetching historical price movements for symbol "{symbol}".')

        cache_key: str = f'{symbol}-data'
        value: SymbolData = self.__cache__.get(cache_key)

        if value is None or ignore_cache:
            warning(f'No item with the key "{cache_key}" existed in the cache.')
            ticker = yf.Ticker(symbol)
            stats = ticker.stats()
            analysis = ticker.analysis
            future_growth_rate: float = analysis.loc['+5Y']['Growth']
            shares_outstanding: float = stats['defaultKeyStatistics']['sharesOutstanding']
            free_cash_flow: float = stats['financialData']['freeCashflow']
            company_name: str = ticker.info['longName']
            annual_dividend_percentage: float = ticker.info['dividendYield']
            eps_ttm: float = ticker.info['trailingEps']
            current_price: float = ticker.info['previousClose']
            pe_ratio: float = ticker.info['forwardPE']
            value: SymbolData = SymbolData(free_cash_flow=free_cash_flow,
                                           future_growth_rate=future_growth_rate,
                                           shares_outstanding=shares_outstanding,
                                           symbol=symbol,
                                           company_name=company_name,
                                           annual_dividend_percentage=annual_dividend_percentage,
                                           eps_ttm=eps_ttm,
                                           current_price=current_price,
                                           pe_ratio=pe_ratio)
            self.__cache__[cache_key] = value
        else:
            info(f'Item for key "{cache_key}" retrieved from cache with value: {value}')

        return value
