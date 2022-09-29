from typing import Optional

from common.enums.bases import Enum
from common.structs.results import BaseResult
from common.utils.strutils import is_int, is_bool


class CryptowatchAssetResult(BaseResult):

    class KEYS(Enum):
        EXTERNAL_ID = 'id'
        SID = 'sid'
        SYMBOL = 'sym'
        NAME = 'name'
        FIAT = 'fiat'
        ROUTE = 'route'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in {k: v for k, v in kwargs.items() if k in self.KEYS}:
            self.set(key, value)

    @property
    def external_id(self) -> Optional[int]:
        return self.get(self.KEYS.EXTERNAL_ID)

    @external_id.setter
    def external_id(self,
                    value: Optional[int]):
        self._set(key=self.KEYS.EXTERNAL_ID, value=value, validate=is_int)

    @property
    def sid(self) -> Optional[str]:
        return self.get(self.KEYS.SID)

    @sid.setter
    def sid(self,
            value: Optional[str]):
        self._set(key=self.KEYS.SID, value=value)

    @property
    def symbol(self) -> Optional[str]:
        return self.get(self.KEYS.SYMBOL)

    @symbol.setter
    def symbol(self,
               value: Optional[str]):
        self._set(key=self.KEYS.SYMBOL, value=value)

    @property
    def name(self) -> Optional[str]:
        return self.get(self.KEYS.NAME)

    @name.setter
    def name(self,
             value: Optional[str]):
        self._set(key=self.KEYS.NAME, value=value)

    @property
    def fiat(self) -> Optional[bool]:
        return self.get(self.KEYS.FIAT)

    @fiat.setter
    def fiat(self, value: Optional[bool]):
        self._set(key=self.KEYS.FIAT, value=value, validate=is_bool)

    @property
    def route(self) -> Optional[str]:
        return self.get(self.KEYS.ROUTE)

    @route.setter
    def route(self,
              value: Optional[str]):
        self._set(key=self.KEYS.ROUTE, value=value)
