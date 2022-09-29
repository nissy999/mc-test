import datetime
from typing import Union, List, Optional, Any, TypeVar, Dict, Type, Callable

from bson.objectid import ObjectId

from DAL.connector import get_collection, DATABASES
from DAL.interfaces import IBaseDbHandler, TID, TIDS, IDbHandlersRouter
from common.consts import LIST_TYPES, MONGODB_ID
from common.enums.bases import Enum
from common.logs.logger import Logger
from common.structs.results import TResultDict
from common.utils.collectionsutils import set_in_dict
from common.utils.strutils import to_ObjectId, is_bool


class BaseDbHandler(IBaseDbHandler):

    ITEM_KEY = '__item__'

    _collection_name: str = None
    _result_cls: Type = None

    class KEYS(Enum):
        ID = MONGODB_ID
        LAST_UPDATE = 'last_update'
        DATE_ADDED = 'date_added'

    _api_to_struct_attributes_mapping: Dict[str, str] = {}

    @classmethod
    def parse_to_result(cls,
                        item: TResultDict,
                        **kwargs) -> TResultDict:
        result: TResultDict = cls._result_cls()

        for api_key, struct_key in cls._api_to_struct_attributes_mapping.items():
            if api_key not in item:
                continue
            set_in_dict(result, struct_key, item.pop(api_key))

        update = {key: value for key, value in item.items() if key not in result}
        if update:
            result.update(update)

        return result

    @classmethod
    def _enrich(cls,
                result: TResultDict,
                now: Optional[datetime.datetime] = None,
                date_added: Optional[Union[bool, datetime.datetime]] = None,
                last_update: Optional[Union[bool, datetime.datetime]] = None,
                **kwargs) -> TResultDict:
        if not isinstance(now, datetime.datetime):
            now = datetime.datetime.utcnow()

        update = {}
        date_added: Optional[datetime.datetime] = date_added if isinstance(date_added, datetime.datetime) else \
            now if date_added is not False else None
        if date_added:
            update[BaseDbHandler.KEYS.DATE_ADDED] = date_added

        last_update: Optional[datetime.datetime] = last_update if isinstance(last_update, datetime.datetime) else \
            now if last_update is not False else None
        if last_update:
            update[BaseDbHandler.KEYS.LAST_UPDATE] = last_update

        if update:
            if isinstance(result, LIST_TYPES):
                [_.update(update) for _ in result]
            else:
                result.update(update)

        return result

    # region insert /save

    @classmethod
    def _pre_insert_validation(cls,
                               result: Union[TResultDict, List[TResultDict]],
                               **kwargs) -> Union[TResultDict, List[TResultDict]]:
        return result

    @classmethod
    def save_to_db(cls,
                   result: Union[TResultDict, List[TResultDict]],
                   enrich: bool = True,
                   now: Optional[datetime.datetime] = None,
                   date_added: Optional[Union[bool, datetime.datetime]] = None,
                   last_update: Optional[Union[bool, datetime.datetime]] = None,
                   func: Callable[[Union[TResultDict, List[TResultDict]]], Union[TResultDict, List[TResultDict]]] = None,
                   **kwargs) -> Union[TResultDict, List[TResultDict]]:
        result = cls._pre_insert_validation(result=result, **kwargs)
        if not result:
            Logger.error_raise(f'result failed validation test')

        multiple = isinstance(result, LIST_TYPES)
        if enrich:
            params = dict(now=now, date_added=date_added, last_update=last_update)
            result = [cls._enrich(_, **params) for _ in result] if multiple else cls._enrich(result, **params)

        if func:
            _result: Union[TResultDict, List[TResultDict]] = func(result)
            return _result

        collection = get_collection(db_name=DATABASES.CRYPTOWATCH,
                                    collection_name=cls._collection_name)
        func = collection.insert_many if multiple else collection.insert_one
        response = func(result)

        if multiple:
            for i in range(len(result)):
                result[i][MONGODB_ID] = response.inserted_ids[i]
        else:
            result[MONGODB_ID] = response.inserted_id

        return result

    insert_to_db = save_to_db

    # endregion insert /save

    # region get

    # get_one for simplicity

    @classmethod
    def get(cls,
            query: Dict[str, Any],
            multiple: bool = True,
            cursor: bool = False,
            limit: Optional[int] = None,
            sort: Optional[Dict[str, int]] = None,
            rdict: bool = False,
            **kwargs) -> Optional[Union[TResultDict, List[TResultDict]]]:
        # projection through kwargs
        if query is None:
            query = {}

        collection = get_collection(db_name=DATABASES.CRYPTOWATCH,
                                    collection_name=cls._collection_name)
        if not multiple:
            result = collection.find_one(query, **kwargs)
            if rdict:
                result = cls.parse_to_result(result)

        else:
            result = collection.find(query, **kwargs)
            if sort:
                result = result.sort(sort)
            if limit:
                result = result.limit(limit)
            if rdict:
                result = [cls.parse_to_result(_) for _ in result]
            elif not cursor:
                result = list(result)

        return result

    @classmethod
    def get_by_id(cls,
                  id_: TID,
                  **kwargs) -> Optional[TResultDict]:
        _id: ObjectId = to_ObjectId(id_[MONGODB_ID] if isinstance(id_, dict) else id_)
        query = {MONGODB_ID: _id}
        result: Optional[TResultDict] = cls.get(query=query, multiple=False, **kwargs)
        return result

    @classmethod
    def get_by_ids(cls,
                   ids: Union[TID, TIDS],
                   multiple: bool = True,
                   **kwargs) -> List[TResultDict]:
        ids: TIDS = [to_ObjectId(_[MONGODB_ID] if isinstance(_, dict) else _) for _ in ids] \
            if isinstance(ids, LIST_TYPES) else [to_ObjectId(ids)]
        if not is_bool(multiple):
            multiple = True
        query = {
            MONGODB_ID: {'$in': ids} if len(ids) > 1 else ids[0]
        }
        result = cls.get(query=query, multiple=multiple, **kwargs)
        return result

    # endregion get

    _dbhandlers_router: Type[IDbHandlersRouter] = None

    @classmethod
    def dbhandlers_router(cls) -> Type[IDbHandlersRouter]:
        if cls._dbhandlers_router is None:
            from DAL.cryptowatch import CryptoWatchDbHandlersRouter
            cls._dbhandlers_router = CryptoWatchDbHandlersRouter
        return cls._dbhandlers_router

