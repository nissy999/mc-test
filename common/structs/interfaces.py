from typing import Optional, Protocol, Any, Callable, Type


class IBaseStruct(Protocol):

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
        raise NotImplementedError()


class IBaseResult(IBaseStruct, Protocol):

    @property
    def success(self) -> Optional[bool]:
        raise NotImplementedError()

    @success.setter
    def success(self,
                value: Optional[bool] = None):
        raise NotImplementedError()


class ICryptoWatchStructsRouter(Protocol):

    @classmethod
    def assets(cls) -> Type[IBaseResult]:
        raise NotImplementedError()

    @classmethod
    def exchanges(cls) -> Type[IBaseResult]:
        raise NotImplementedError()

    @classmethod
    def markets(cls) -> Type[IBaseResult]:
        raise NotImplementedError()

    @classmethod
    def pairs(cls) -> Type[IBaseResult]:
        raise NotImplementedError()

    @classmethod
    def prices(cls) -> Type[IBaseResult]:
        raise NotImplementedError()
