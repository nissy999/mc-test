import copy
import datetime
from typing import Union, Dict, Optional, Callable, List

from DAL.bases import BaseDbHandler
from DAL.connector import get_collection
from common.consts import MONGODB_ID, LIST_TYPES
from common.structs.cryptowatch.assets import CryptowatchAssetResult
from common.structs.results import TResultDict
from common.utils.strutils import is_bool

ASSET_KEYS = CryptowatchAssetResult.KEYS


class AssetsDbHandler(BaseDbHandler):

    _collection_name = 'CryptoWatchAssets'
    _result_cls = CryptowatchAssetResult

    _api_to_struct_attributes_mapping: Dict[str, str] = {
        'id': 'external_id',
        'sid': 'sid',
        'symbol': 'symbol',
        'name': 'name',
        'fiat': 'fiat',
    }

    @classmethod
    def get_by_external_id(cls,
                           external_id: Union[int, str, List[int], List[str]],
                           multiple: bool = None,
                           **kwargs):
        if isinstance(external_id, LIST_TYPES):
            query = {'$in': list(set(int(_) for _ in external_id))}
            if not is_bool(multiple):
                multiple = True
        else:
            query = int(external_id)
            if not is_bool(multiple):
                multiple = False
        query = {ASSET_KEYS.EXTERNAL_ID: query}

        return cls.get(query=query, multiple=multiple, **kwargs)

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

        collection = get_collection(collection_name=cls._collection_name)

        def handle_asset(asset: TResultDict) -> TResultDict:
            external_id: int = \
                asset.external_id if isinstance(asset, CryptowatchAssetResult) else asset[ASSET_KEYS.EXTERNAL_ID]

            if enrich:
                asset = cls._enrich(asset)

            db_asset = cls.get_by_external_id(external_id)
            if db_asset:
                # do smarter update
                asset.pop(MONGODB_ID, None)
                update = copy.deepcopy(dict(asset))
                update[cls.KEYS.LAST_UPDATE] = datetime.datetime.utcnow()
                update = {'$set': update}

                unset = [
                    _ for _ in db_asset
                    if _ not in (MONGODB_ID, cls.KEYS.DATE_ADDED, cls.KEYS.LAST_UPDATE, 'markets')
                    and _ not in asset
                ]
                if unset:
                    update['$unset'] = {_: '' for _ in unset}

                _result = collection.update_one({MONGODB_ID: db_asset[MONGODB_ID]}, update)
                asset[MONGODB_ID] = db_asset[MONGODB_ID]
            else:
                insert_results.append(asset)

            return asset

        if isinstance(result, dict):
            result = handle_asset(result)
        else:
            for i, asset in enumerate(result):
                # if i % 100 == 0:
                #     print(f'handled {i} assets')
                result[i] = handle_asset(asset)
            # result = [handle_asset(_) for _ in result]

        if insert_results:
            _result = collection.insert_many(result)
            for i in range(len(result)):
                result[i][MONGODB_ID] = _result.inserted_ids[i]

        return result







