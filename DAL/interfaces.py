import datetime
from abc import abstractmethod
from typing import Protocol, Optional, Union, List, Dict, Any, TypeVar, Type

from bson import ObjectId

from common.interfaces import IBaseRouter
from common.structs.results import TResultDict


TID = TypeVar('TID', bound=Union[ObjectId, str, Dict[str, Any]])

TIDS = TypeVar('TIDS', bound=List[TID])


class IBaseDbHandler(Protocol):

    @classmethod
    def _enrich(cls,
                result: TResultDict,
                now: Optional[datetime.datetime] = None,
                date_added: Optional[Union[bool, datetime.datetime]] = None,
                last_update: Optional[Union[bool, datetime.datetime]] = None):
        raise NotImplementedError()

    @classmethod
    def parse_to_result(cls,
                        item: TResultDict,
                        result_cls: Type,
                        **kwargs) -> TResultDict:
        raise NotImplementedError()

    # region insert /save

    @classmethod
    def _pre_insert_validation(cls,
                               result: Union[TResultDict, List[TResultDict]],
                               **kwargs) -> Union[TResultDict, List[TResultDict]]:
        raise NotImplementedError()

    @classmethod
    def save_to_db(cls,
                   result: Union[TResultDict, List[TResultDict]],
                   enrich: bool = True,
                   now: Optional[datetime.datetime] = None,
                   date_added: Optional[Union[bool, datetime.datetime]] = None,
                   last_update: Optional[Union[bool, datetime.datetime]] = None,
                   **kwargs):
        raise NotImplementedError()

    insert_to_db = save_to_db

    # endregion insert /save

    # region get

    @classmethod
    def get(cls,
            query: Dict[str, Any],
            multiple: bool = True,
            cursor: bool = False,
            limit: Optional[int] = None,
            sort: Optional[Dict[str, int]] = None,
            rdict: bool = False,
            **kwargs) -> Optional[Union[TResultDict, List[TResultDict]]]:
        raise NotImplementedError()

    @classmethod
    def get_by_id(cls,
                  id_: TID,
                  **kwargs) -> Optional[TResultDict]:
        raise NotImplementedError()

    @classmethod
    def get_by_ids(cls,
                   ids: Union[TID, TIDS],
                   multiple: bool = True,
                   **kwargs) -> List[TResultDict]:
        raise NotImplementedError()

    # endregion get

    @classmethod
    def dbhandlers_router(cls):
        raise NotImplementedError()


class IDbHandlersRouter(IBaseRouter, Protocol):

    __item_interface__ = IBaseDbHandler

    # @classmethod
    # def assets(cls) -> Type[IBaseDbHandler]:
    #     raise NotImplementedError()
    #
    # @classmethod
    # def exchanges(cls) -> Type[IBaseDbHandler]:
    #     raise NotImplementedError()
    #
    # @classmethod
    # def markets(cls) -> Type[IBaseDbHandler]:
    #     raise NotImplementedError()
    #
    # @classmethod
    # def pairs(cls) -> Type[IBaseDbHandler]:
    #     raise NotImplementedError()
    #
    # @classmethod
    # def prices(cls) -> Type[IBaseDbHandler]:
    #     raise NotImplementedError()

