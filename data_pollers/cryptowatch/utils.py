from typing import Type, TypeVar, Union

from common.interfaces import IBaseRouter
from data_pollers.bases import BaseDataPoller


class CryptoWatchPollersRouter(IBaseRouter):

    __item_interface__ = BaseDataPoller

    TBaseDataPoller = TypeVar('TBaseDataPoller', bound=BaseDataPoller)

    _assets: 'TBaseDataPoller' = None

    @classmethod
    def assets(cls, **kwargs) -> 'TBaseDataPoller':
        if cls._assets is None:
            from data_pollers.cryptowatch.assets import CryptowatchAssetsPoller
            cls._assets = CryptowatchAssetsPoller
        return cls._assets(**kwargs)

    _exchanges: 'TBaseDataPoller' = None

    @classmethod
    def exchanges(cls, **kwargs) -> 'TBaseDataPoller':
        if not cls._exchanges:
            from data_pollers.cryptowatch.exchanges import CryptowatchExchangesPoller
            cls._exchanges = CryptowatchExchangesPoller
        return cls._exchanges(**kwargs)

    _markets: 'TBaseDataPoller' = None

    @classmethod
    def markets(cls, **kwargs) -> 'TBaseDataPoller':
        if not cls._markets:
            from data_pollers.cryptowatch.markets import CryptowatchMarketsPoller
            cls._markets = CryptowatchMarketsPoller
        return cls._markets(**kwargs)

    _pairs: 'TBaseDataPoller' = None

    @classmethod
    def pairs(cls, **kwargs) -> 'TBaseDataPoller':
        if not cls._pairs:
            from data_pollers.cryptowatch.pairs import CryptowatchAssetsPairsPoller
            cls._pairs = CryptowatchAssetsPairsPoller
        return cls._pairs(**kwargs)

    _prices: 'TBaseDataPoller' = None

    @classmethod
    def prices(cls, **kwargs) -> 'TBaseDataPoller':
        if not cls._prices:
            from data_pollers.cryptowatch.prices import CryptowatchPricesPoller
            cls._prices = CryptowatchPricesPoller
        return cls._prices(**kwargs)
