'''This module defines valuation engine components.'''
from frostaura.models.valuation_result import ValuationResult

class IAssetValuationEngine:
    '''Component to perform functions related to asset valuation.'''

    def valuate(self, symbol: str) -> ValuationResult:
        '''Valuate a given asset.'''

        raise NotImplementedError()
