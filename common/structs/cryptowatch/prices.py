from typing import Optional, Union, Dict, Any

from bson import ObjectId

from common.consts import MONGODB_ID, UNDEFINED
from common.enums.bases import Enum
from common.structs.results import BaseResult
from common.utils.strutils import is_int, to_ObjectId


class CryptowatchPriceResult(BaseResult):

    class KEYS(Enum):
        PRICE = 'price'
        
        PAIR_ID = f'base.{MONGODB_ID}'
        PAIR_EXTERNAL_ID = 'base.id'
        PAIR_SYMBOL = 'base.symbol'

        EXCHANGE_ID = f'exchange.{MONGODB_ID}'
        EXCHANGE_EXTERNAL_ID = 'exchange.id'
        EXCHANGE_SYMBOL = 'exchange.symbol'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in {k: v for k, v in kwargs.items() if k in self.KEYS}:
            self.set(key, value)
        self._pair: Optional[Dict[str, Any]] = UNDEFINED
        self._exchange: Optional[Dict[str, Any]] = UNDEFINED

    @property
    def pair_id(self) -> Optional[ObjectId]:
        return self.get(self.KEYS.PAIR_ID)

    @pair_id.setter
    def pair_id(self,
                value: Optional[Union[ObjectId, str]]):
        self._set(key=self.KEYS.PAIR_ID, value=value, trans=to_ObjectId, reset='_pair')

    @property
    def pair(self) -> Optional[Dict[str, Any]]:
        if self._pair == UNDEFINED:
            if self.pair_id:
                from DAL.cryptowatch import CryptoWatchDbHandlersRouter as _C
                self._pair: Optional[Dict[str, Any]] = _C.pairs().get_by_id(self.pair_id, rdict=True)
            else:
                self._pair = None
        return self._pair

    @property
    def pair_external_id(self) -> Optional[int]:
        return self.get(self.KEYS.PAIR_EXTERNAL_ID)

    @pair_external_id.setter
    def pair_external_id(self,
                         value: Optional[int]):
        self._set(key=self.KEYS.PAIR_EXTERNAL_ID, value=value, validate=is_int)

    @property
    def pair_symbol(self) -> Optional[str]:
        return self.get(self.KEYS.PAIR_SYMBOL)

    @pair_symbol.setter
    def pair_symbol(self,
                    value: Optional[str]):
        self._set(key=self.KEYS.PAIR_SYMBOL, value=value)

    @property
    def exchange_id(self) -> Optional[ObjectId]:
        return self.get(self.KEYS.EXCHANGE_ID)

    @exchange_id.setter
    def exchange_id(self,
                    value: Optional[Union[ObjectId, str]]):
        self._set(key=self.KEYS.EXCHANGE_ID, value=value, trans=to_ObjectId, reset='_exchange')

    @property
    def exchange(self) -> Optional[Dict[str, Any]]:
        if self._exchange == UNDEFINED:
            if self.exchange_id:
                from DAL.cryptowatch import CryptoWatchDbHandlersRouter as _C
                self._exchange: Optional[Dict[str, Any]] = \
                    _C.exchanges().get_by_id(self.exchange_id, rdict=True)
            else:
                self._exchange = None
        return self._exchange

    @property
    def exchange_external_id(self) -> Optional[int]:
        return self.get(self.KEYS.EXCHANGE_EXTERNAL_ID)

    @exchange_external_id.setter
    def exchange_external_id(self,
                             value: Optional[int]):
        self._set(key=self.KEYS.EXCHANGE_EXTERNAL_ID, value=value, validate=is_int)

    @property
    def exchange_symbol(self) -> Optional[str]:
        return self.get(self.KEYS.EXCHANGE_SYMBOL)

    @exchange_symbol.setter
    def exchange_symbol(self,
                        value: Optional[str]):
        self._set(key=self.KEYS.EXCHANGE_SYMBOL, value=value)

    @property
    def price(self) -> Optional[float]:
        return self.get(self.KEYS.PRICE)

    @price.setter
    def price(self,
              value: Optional[float]):
        self._set(key=self.KEYS.PRICE, value=value, validate=lambda x: isinstance(x, float) and x >= 0)
