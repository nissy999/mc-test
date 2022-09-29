from typing import Type

from common.interfaces import IBaseRouter
from common.structs.interfaces import IBaseResult, ICryptoWatchStructsRouter


class CryptoWatchStructsRouter(IBaseRouter):

    __item_interface__: Type[IBaseResult] = IBaseResult

    _assets: Type[IBaseResult] = None

    @classmethod
    def assets(cls) -> Type[IBaseResult]:
        if cls._assets is None:
            from common.structs.cryptowatch.assets import CryptowatchAssetResult
            cls._assets = CryptowatchAssetResult
        return cls._assets

    _exchanges: Type[IBaseResult] = None

    @classmethod
    def exchanges(cls) -> Type[IBaseResult]:
        if not cls._exchanges:
            from common.structs.cryptowatch.exchanges import CryptowatchExchangeResult
            cls._exchanges = CryptowatchExchangeResult
        return cls._exchanges

    _markets: Type[IBaseResult] = None

    @classmethod
    def markets(cls) -> Type[IBaseResult]:
        if not cls._markets:
            from common.structs.cryptowatch.markets import CryptowatchMarketResult
            cls._markets = CryptowatchMarketResult
        return cls._markets

    _pairs: Type[IBaseResult] = None

    @classmethod
    def pairs(cls) -> Type[IBaseResult]:
        if not cls._pairs:
            from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult
            cls._pairs = CryptowatchAssetsPairResult
        return cls._pairs

    _prices: Type[IBaseResult] = None

    @classmethod
    def prices(cls) -> Type[IBaseResult]:
        if not cls._prices:
            from common.structs.cryptowatch.prices import CryptowatchPriceResult
            cls._prices = CryptowatchPriceResult
        return cls._prices
