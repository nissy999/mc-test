import copy
from typing import Dict, Union, List, TypeVar, Any


class _EnumMeta(type):

    __MAPPING__: str = '__mapping__'
    __SUPPORTED_VALUE_TYPES__: List[type] = [str, int, float, bool]
    __TMAPPING__ = TypeVar('__TMAPPING__', bound=Dict[str, Union['__SUPPORTED_VALUE_TYPES__']])

    def __new__(cls, name, bases, dct):
        dct[cls.__MAPPING__]: 'cls.__TMAPPING__' = {
            k: v
            for k, v in dct.items()
            if not k.startswith('__') and
            isinstance(v, tuple(cls.__SUPPORTED_VALUE_TYPES__))
        }
        return super().__new__(cls, name, bases, dct)

    def _update_mapping_(cls,
                         update):
        getattr(cls, cls.__MAPPING__).update(update)

    def keys_generator(cls):
        for item in getattr(cls, cls.__MAPPING__):
            yield item

    def keys(cls):
        """
        Returns the list of keys of the enum
        :return:
        """
        return list(cls.keys_generator())

    names = keys

    def values_generator(cls):
        mapping: Dict[str, Union['cls.__SUPPORTED_VALUE_TYPES__']] = getattr(cls, cls.__MAPPING__)
        for value in mapping.values():
            yield value

    def values(cls):
        """
        Returns the list of values
        :return:
        """
        return list(cls.values_generator())

    def __len__(cls):
        return len(cls.mapping(noclone=True))

    def mapping(cls,
                noclone: bool = False) -> Dict[str, '__SUPPORTED_VALUE_TYPES__']:
        mapping: Dict[str, 'cls.__SUPPORTED_VALUE_TYPES__'] = getattr(cls, cls.__MAPPING__)
        return copy.deepcopy(mapping) if not noclone else mapping

    def get_name(cls,
                 value: Union['__SUPPORTED_VALUE_TYPES__']):
        return next(k for k, v in cls.mapping(noclone=True).items() if v == value)

    def __contains__(cls, value):
        return True if cls.get_name(value) else False  # will raise exception if value is not found

    def __iter__(cls):
        for k, v in cls.mapping(noclone=True).items():
            yield v

    def is_value(cls,
                 value: '__SUPPORTED_VALUE_TYPES__') -> bool:
        return next((True for _ in cls.values_generator() if _ == value), False)

    def get_value(cls,
                  value: '__SUPPORTED_VALUE_TYPES__') -> Any:
        return next(_ for _ in cls.values_generator() if _ == value)

    def is_key(cls,
               key: str) -> bool:
        return next((True for _ in cls.keys_generator() if _ == key), False)

    def get_key(cls,
                key: str) -> str:
        return next(_ for _ in cls.keys_generator() if _ == key)


class Enum(metaclass=_EnumMeta):
    """
    Base class for enums in the system. All functionality is implemented in the metaclass
    """
    pass
