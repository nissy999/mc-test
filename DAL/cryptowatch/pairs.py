import copy
import datetime
from typing import Union, Optional, List, Callable, Dict, Any

from bson import ObjectId

from DAL.bases import BaseDbHandler
from DAL.connector import get_collection
from common.consts import MONGODB_ID
from common.logs.logger import Logger
from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult
from common.structs.results import TResultDict, BaseResult
from common.utils.collectionsutils import set_in_dict, get_from_dict

PAIR_KEYS = CryptowatchAssetsPairResult.KEYS


class PairsDbHandler(BaseDbHandler):

    _collection_name = 'CryptoWatchPairs'
    _result_cls = CryptowatchAssetsPairResult

    @classmethod
    def get_by_external_id(cls,
                           external_id: Union[int, str],
                           **kwargs) -> Optional[TResultDict]:
        query = {
            PAIR_KEYS.EXTERNAL_ID: int(external_id)
        }
        return cls.get(query=query, multiple=False, **kwargs)

    @classmethod
    def get_by_symbol(cls,
                      symbol: str,
                      multiple: Optional[bool] = True,
                      **kwargs) -> Optional[Union[TResultDict, List[TResultDict]]]:
        query = {
            PAIR_KEYS.SYMBOL: symbol
        }
        return cls.get(query=query, multiple=multiple, **kwargs)

    @classmethod
    def _enrich(cls,
                result: TResultDict,
                now: Optional[datetime.datetime] = None,
                date_added: Optional[Union[bool, datetime.datetime]] = None,
                last_update: Optional[Union[bool, datetime.datetime]] = None,
                **kwargs) -> TResultDict:
        result = super()._enrich(result=result, now=now, date_added=date_added, last_update=last_update, **kwargs)

        # foreign keys constraints implementation
        # cache instead of direct access
        params = {'projection': {MONGODB_ID: 1}}

        base_id = get_from_dict(result, PAIR_KEYS.BASE_ID)
        if base_id:
            base_asset = cls.dbhandlers_router().assets().get_by_id(base_id, **params)
        else:
            base_id = get_from_dict(result, key=PAIR_KEYS.BASE_EXTERNAL_ID)
            if base_id:
                base_asset = cls.dbhandlers_router().assets().get_by_external_id(base_id, **params)
            else:
                base_id = get_from_dict(result, PAIR_KEYS.BASE_SYMBOL)
                if not base_id:
                    Logger.error_raise(f'no base id can be found - cannot enrich pair')
                base_asset = cls.dbhandlers_router().assets().get_by_symbol(base_id, **params)
        set_in_dict(result, PAIR_KEYS.BASE_ID, base_asset[MONGODB_ID])

        quote_id = get_from_dict(result, PAIR_KEYS.QUOTE_ID)
        if quote_id:
            quote_asset = cls.dbhandlers_router().assets().get_by_id(quote_id, **params)
        else:
            quote_id = get_from_dict(result, key=PAIR_KEYS.QUOTE_EXTERNAL_ID)
            if quote_id:
                quote_asset = cls.dbhandlers_router().assets().get_by_external_id(quote_id, **params)
            else:
                quote_id = get_from_dict(result, PAIR_KEYS.QUOTE_SYMBOL)
                if not quote_id:
                    Logger.error_raise(f'no quote id can be found - cannot enrich pair')
                quote_asset = cls.dbhandlers_router().assets().get_by_symbol(quote_id, **params)
        set_in_dict(result, PAIR_KEYS.QUOTE_ID, quote_asset[MONGODB_ID])

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

        insert_results: List[TResultDict] = []

        # if enrich:
        #     if isinstance(result, dict):
        #         assets_ids = {result.external_id if isinstance(result, CryptowatchAssetsPairResult) else
        #                       get_from_dict(result, PAIR_KEYS.EXTERNAL_ID)}
        #         quote_ids = {result.quote_external_id if isinstance(result, CryptowatchAssetsPairResult) else
        #                      get_from_dict(result, PAIR_KEYS.QUOTE_EXTERNAL_ID)}
        #     else:
        #         assets_ids = {pair.external_id if isinstance(pair, CryptowatchAssetsPairResult) else
        #                       get_from_dict(pair, PAIR_KEYS.EXTERNAL_ID) for pair in result}
        #         quote_ids = {pair.quote_external_id if isinstance(pair, CryptowatchAssetsPairResult)
        #                      else get_from_dict(pair, PAIR_KEYS.QUOTE_EXTERNAL_ID) for pair in result}
        #     assets_ids = assets_ids.union(quote_ids)
        #     assets = cls.dbhandlers_router().assets().get_by_external_id(assets_ids)
        #     assets_by_ids = {_[MONGODB_ID]: _ for _ in assets}
        # else:
        #     assets_by_ids = {}

        collection = get_collection(collection_name=cls._collection_name)

        def handle_pair(pair: TResultDict) -> TResultDict:
            external_id: int = pair.external_id if isinstance(pair, CryptowatchAssetsPairResult) else \
                get_from_dict(pair, PAIR_KEYS.EXTERNAL_ID)

            if enrich:
                pair = cls._enrich(pair)

            db_pair = cls.get_by_external_id(external_id)
            if db_pair:
                # do smarter update
                pair.pop(MONGODB_ID, None)
                update = copy.deepcopy(dict(pair))
                update[cls.KEYS.LAST_UPDATE] = datetime.datetime.utcnow()
                update = {'$set': update}

                unset = [
                    _ for _ in db_pair
                    if _ not in (MONGODB_ID, cls.KEYS.DATE_ADDED, cls.KEYS.LAST_UPDATE)
                    and _ not in pair
                ]
                if unset:
                    update['$unset'] = {_: '' for _ in unset}

                _result = collection.update_one({MONGODB_ID: db_pair[MONGODB_ID]}, update)
                pair[MONGODB_ID] = db_pair[MONGODB_ID]
            else:
                insert_results.append(pair)

            return pair

        if isinstance(result, dict):
            result = handle_pair(result)
        else:
            for i, pair in enumerate(result):
                # if i % 100 == 0:
                #     print(f'handled {i} pairs')
                result[i] = handle_pair(pair)

            result = [handle_pair(_) for _ in result]

        if insert_results:
            _result = collection.insert_many(result)
            for i in range(len(result)):
                result[i][MONGODB_ID] = _result.inserted_ids[i]
            # result = [handle_asset(_) for _ in result]

        return result

    @classmethod
    def get_by_base_asset(cls,
                          symbol: str,
                          quote_symbol: Optional[str] = None,
                          multiple: bool = True,
                          **kwargs) -> Union[TResultDict, List[TResultDict]]:
        query = {
            CryptowatchAssetsPairResult.KEYS.BASE_SYMBOL: symbol
        }
        if quote_symbol:
            query[CryptowatchAssetsPairResult.KEYS.QUOTE_SYMBOL] = quote_symbol

        result = cls.dbhandlers_router().assets().get(query=query, multiple=multiple, **kwargs)
        return result
