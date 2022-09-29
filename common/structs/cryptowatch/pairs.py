from typing import Optional, Union, Dict, Any

from bson import ObjectId

from common.consts import MONGODB_ID, UNDEFINED
from common.enums.bases import Enum
from common.structs.results import BaseResult
from common.utils.strutils import is_int, to_ObjectId


class CryptowatchAssetsPairResult(BaseResult):

    class KEYS(Enum):
        EXTERNAL_ID = 'id'
        SYMBOL = 'symbol'
        ROUTE = 'route'

        BASE_ID = f'base.{MONGODB_ID}'
        BASE_EXTERNAL_ID = 'base.id'
        BASE_SID = 'base.sid'
        BASE_SYMBOL = 'base.symbol'

        QUOTE_ID = f'quote.{MONGODB_ID}'
        QUOTE_EXTERNAL_ID = 'quote.id'
        QUOTE_SID = 'quote.sid'
        QUOTE_SYMBOL = 'quote.symbol'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in {k: v for k, v in kwargs.items() if k in self.KEYS}:
            self.set(key, value)
        self._base_asset: Optional[Dict[str, Any]] = UNDEFINED
        self._quote_asset: Optional[Dict[str, Any]] = UNDEFINED

    @property
    def external_id(self) -> Optional[int]:
        return self.get(self.KEYS.EXTERNAL_ID)

    @external_id.setter
    def external_id(self,
                    value: Optional[int]):
        self._set(key=self.KEYS.EXTERNAL_ID, value=value, validate=is_int)

    @property
    def symbol(self) -> Optional[str]:
        return self.get(self.KEYS.SYMBOL)

    @symbol.setter
    def symbol(self,
               value: Optional[str]):
        self._set(key=self.KEYS.SYMBOL, value=value)

    @property
    def base_id(self) -> Optional[ObjectId]:
        return self.get(self.KEYS.BASE_ID)

    @base_id.setter
    def base_id(self,
                value: Optional[Union[ObjectId, str]]):
        self._set(key=self.KEYS.BASE_ID, value=value, trans=to_ObjectId, reset='_base_asset')

    @property
    def base_asset(self) -> Optional[Dict[str, Any]]:
        if self._base_asset == UNDEFINED:
            if self.base_id:
                from DAL.cryptowatch import CryptoWatchDbHandlersRouter as _C
                self._base_asset: Optional[Dict[str, Any]] = _C.assets().get_by_id(self.base_id, rdict=True)
            else:
                self._base_asset = None
        return self._base_asset

    @property
    def base_external_id(self) -> Optional[int]:
        return self.get(self.KEYS.BASE_EXTERNAL_ID)

    @base_external_id.setter
    def base_external_id(self,
                         value: Optional[int]):
        self._set(key=self.KEYS.BASE_EXTERNAL_ID, value=value, validate=is_int)

    @property
    def base_sid(self) -> Optional[str]:
        return self.get(self.KEYS.BASE_SID)

    @base_sid.setter
    def base_sid(self,
                 value: Optional[str]):
        self._set(key=self.KEYS.BASE_SID, value=value)

    @property
    def base_symbol(self) -> Optional[str]:
        return self.get(self.KEYS.BASE_SYMBOL)

    @base_symbol.setter
    def base_symbol(self,
                    value: Optional[str]):
        self._set(key=self.KEYS.BASE_SYMBOL, value=value)

    @property
    def quote_id(self) -> Optional[ObjectId]:
        return self.get(self.KEYS.QUOTE_ID)

    @quote_id.setter
    def quote_id(self,
                 value: Optional[Union[ObjectId, str]]):
        self._set(key=self.KEYS.QUOTE_ID, value=value, trans=to_ObjectId, reset='_quote_asset')

    @property
    def quote_asset(self) -> Optional[Dict[str, Any]]:
        if self._quote_asset == UNDEFINED:
            if self.quote_id:
                from DAL.cryptowatch import CryptoWatchDbHandlersRouter as _C
                self._quote_asset: Optional[Dict[str, Any]] = _C.assets().get_by_id(self.quote_id, rdict=True)
            else:
                self._quote_asset = None
        return self._quote_asset

    @property
    def quote_external_id(self) -> Optional[int]:
        return self.get(self.KEYS.QUOTE_EXTERNAL_ID)

    @quote_external_id.setter
    def quote_external_id(self,
                          value: Optional[int]):
        self._set(key=self.KEYS.QUOTE_EXTERNAL_ID, value=value, validate=is_int)

    @property
    def quote_sid(self) -> Optional[int]:
        return self.get(self.KEYS.QUOTE_SID)

    @quote_sid.setter
    def quote_sid(self,
                  value: Optional[str]):
        self._set(key=self.KEYS.QUOTE_SID, value=value)

    @property
    def quote_symbol(self) -> Optional[str]:
        return self.get(self.KEYS.QUOTE_SYMBOL)

    @quote_symbol.setter
    def quote_symbol(self,
                     value: Optional[str]):
        self._set(key=self.KEYS.QUOTE_SYMBOL, value=value)

    @property
    def route(self) -> Optional[str]:
        return self.get(self.KEYS.ROUTE)

    @route.setter
    def route(self,
              value: Optional[str]):
        self._set(key=self.KEYS.ROUTE, value=value)
