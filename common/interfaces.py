from typing import Protocol, Optional, Type


class IBaseRouter(Protocol):

    __item_interface__: Type

    @classmethod
    def assets(cls) -> Type['__item_interface__']:
        raise NotImplementedError()

    @classmethod
    def exchanges(cls) -> Type['__item_interface__']:
        raise NotImplementedError()

    @classmethod
    def markets(cls) -> Type['__item_interface__']:
        raise NotImplementedError()

    @classmethod
    def pairs(cls) -> Type['__item_interface__']:
        raise NotImplementedError()

    @classmethod
    def prices(cls) -> Type['__item_interface__']:
        raise NotImplementedError()
