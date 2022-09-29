from typing import Optional, Any, Dict, Callable

from common.consts import UNDEFINED
from common.logs.logger import Logger
from common.structs.interfaces import IBaseStruct
from common.utils.collectionsutils import RDict
from common.utils.strutils import is_bool


class BaseStruct(RDict, IBaseStruct):

    _DEFAULTS = {
        'pop': True
    }

    def _set(self,
             key: str,
             value: Optional[Any] = None,
             pop: Optional[bool] = None,
             validate: Optional[Callable[[Any], Any]] = None,
             trans: Optional[Callable[[Any], Any]] = None,
             reset: Optional[str] = None,
             **kwargs):
        """
        Sets or removes an attribute from the object's dict.
        Supports nested attributes (dot notation)
        :param key: the key to set/remove
        :param value: the value to set/remove
        :param pop: indicates whether to remove the key if the value is None
        :param validate: an optional callable which validates the value
        :param trans: an optional callable which transforms the value to another scalar value
        :param reset: an options string representing an attribute of the current object which value should be reseted
        :param kwargs:
        :return:
        """
        if value is None:
            if not is_bool(pop):
                pop = self._DEFAULTS['pop']
            if pop:
                self.pop(key, None)
            else:
                self[key] = None

            if reset:
                setattr(self, reset, UNDEFINED)
        else:
            if trans:
                value = trans(value)
            if validate and not validate(value):
                Logger.error_raise(f'value failed validation test - key: "{key}"')
            self.set(key, value)
