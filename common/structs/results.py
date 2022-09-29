from typing import Optional, TypeVar, Union, Any, Dict

from common.enums.bases import Enum
from common.structs.bases import BaseStruct
from common.structs.interfaces import IBaseResult
from common.utils.strutils import is_bool


class BaseResult(BaseStruct, IBaseResult):

    class KEYS(Enum):
        SUCCESS = 'success'

    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)

        update = {k: v for k, v in kwargs.items() if k in self.KEYS}
        if update:
            self.update(update)
        # for key, value in {k: v for k, v in kwargs.items() if k in self.KEYS}.items():
        #     self.set(key, value)

    @property
    def success(self) -> Optional[bool]:
        return self.get(self.KEYS.SUCCESS)

    @success.setter
    def success(self,
                value: Optional[bool] = None):
        self._set(key=self.KEYS.SUCCESS, value=value, validate=is_bool)


TResult = TypeVar('TResult', bound=Union[BaseResult, IBaseResult])

TResultDict = TypeVar('TResultDict', bound=Union[BaseResult, Dict[str, Any]])
