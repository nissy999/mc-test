from typing import Optional

from common.enums.bases import Enum
from common.structs.results import BaseResult
from common.utils.strutils import is_int, is_bool


class CryptowatchExchangeResult(BaseResult):

    class KEYS(Enum):
        EXTERNAL_ID = 'id'
        NAME = 'name'
        SYMBOL = 'symbol'
        ACTIVE = 'active'
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
    def name(self) -> Optional[str]:
        return self.get(self.KEYS.NAME)

    @name.setter
    def name(self,
             value: Optional[str]):
        self._set(key=self.KEYS.NAME, value=value, trans=lambda x: x.strip())

    @property
    def active(self) -> Optional[bool]:
        return self.get(self.KEYS.ACTIVE)

    @active.setter
    def active(self,
               value: Optional[bool]):
        self._set(key=self.KEYS.ACTIVE, value=value, validate=is_bool)

    @property
    def route(self) -> Optional[str]:
        return self.get(self.KEYS.ROUTE)

    @route.setter
    def route(self,
              value: Optional[str]):
        self._set(key=self.KEYS.ROUTE, value=value)

