from typing import Type

from DAL.interfaces import IBaseDbHandler, IDbHandlersRouter


class CryptoWatchDbHandlersRouter(IDbHandlersRouter):

    _assets: Type[IBaseDbHandler] = None

    @classmethod
    def assets(cls) -> Type[IBaseDbHandler]:
        if cls._assets is None:
            from DAL.cryptowatch.assets import AssetsDbHandler
            cls._assets = AssetsDbHandler
        return cls._assets

    _exchanges: Type[IBaseDbHandler] = None

    @classmethod
    def exchanges(cls) -> Type[IBaseDbHandler]:
        if not cls._exchanges:
            from DAL.cryptowatch.exchanges import ExchangesDbHandler
            cls._exchanges = ExchangesDbHandler
        return cls._exchanges

    _markets: Type[IBaseDbHandler] = None

    @classmethod
    def markets(cls) -> Type[IBaseDbHandler]:
        if not cls._markets:
            from DAL.cryptowatch.markets import MarketsDbHandler
            cls._markets = MarketsDbHandler
        return cls._markets

    _pairs: Type[IBaseDbHandler] = None

    @classmethod
    def pairs(cls) -> Type[IBaseDbHandler]:
        if not cls._pairs:
            from DAL.cryptowatch.pairs import PairsDbHandler
            cls._pairs = PairsDbHandler
        return cls._pairs

    _prices: Type[IBaseDbHandler] = None

    @classmethod
    def prices(cls) -> Type[IBaseDbHandler]:
        if not cls._prices:
            from DAL.cryptowatch.prices import PricesDbHandler
            cls._prices = PricesDbHandler
        return cls._prices
