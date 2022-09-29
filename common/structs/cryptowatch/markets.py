from typing import Optional

from common.consts import MONGODB_ID
from common.enums.bases import Enum
from common.structs.results import BaseResult
from common.utils.strutils import is_int


class CryptowatchMarketResult(BaseResult):

    class KEYS(Enum):
        EXTERNAL_ID = 'id'

        EXCHANGE_ID = f'exchange.{MONGODB_ID}'
        EXCHANGE_EXTERNAL_ID = 'exchange.id'
        EXCHANGE_SYMBOL = 'exchange.symbol'

        PAIR_ID = f'pair.{MONGODB_ID}'
        PAIR_EXTERNAL_ID = 'pair.id'
        PAIR_SYMBOL = 'pair.symbol'

        ROUTE = 'route'
        ACTIVE = 'active'

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
        self._set(key=self.KEYS.EXTERNAL_ID, value=value, trans=is_int)

    @property
    def exchange_id(self) -> Optional[int]:
        return self.get(self.KEYS.EXCHANGE_ID)

    @exchange_id.setter
    def exchange_id(self,
                    value: Optional[int]):
        self._set(key=self.KEYS.EXCHANGE_ID, value=value, validate=is_int)

    @property
    def exchange_symbol(self) -> Optional[str]:
        return self.get(self.KEYS.EXCHANGE_SYMBOL)

    @exchange_symbol.setter
    def exchange_symbol(self,
                        value: Optional[str]):
        self._set(key=self.KEYS.EXCHANGE_SYMBOL, value=value)

    @property
    def pair_id(self) -> Optional[int]:
        return self.get(self.KEYS.PAIR_ID)

    @pair_id.setter
    def pair_id(self,
                value: Optional[int]):
        self._set(key=self.KEYS.PAIR_ID, value=value, validate=is_int)

    @property
    def pair_symbol(self) -> Optional[str]:
        return self.get(self.KEYS.PAIR_SYMBOL)

    @pair_symbol.setter
    def pair_symbol(self,
                    value: Optional[str]):
        self._set(key=self.KEYS.PAIR_SYMBOL, value=value)

