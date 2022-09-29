import datetime
from typing import Union, Optional, List

from bson import ObjectId

from DAL.bases import BaseDbHandler
from common.consts import MONGODB_ID
from common.structs.cryptowatch.prices import CryptowatchPriceResult
from common.structs.results import TResultDict
from common.utils.strutils import is_ObjectId, to_ObjectId, is_int

PRICE_KEYS = CryptowatchPriceResult.KEYS


class PricesDbHandler(BaseDbHandler):

    _collection_name = 'CryptoWatchPrices'
    _result_cls = CryptowatchPriceResult

    _api_to_struct_attributes_mapping = {
        'price': PRICE_KEYS.PRICE,
        f'base.{MONGODB_ID}': PRICE_KEYS.PAIR_ID,

        'base.id': PRICE_KEYS.PAIR_EXTERNAL_ID,
        'base.symbol': PRICE_KEYS.PAIR_SYMBOL,

        'exchange.id': PRICE_KEYS.EXCHANGE_EXTERNAL_ID,
        'exchange.symbol': PRICE_KEYS.EXCHANGE_SYMBOL
    }

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

        # projection = {MONGODB_ID: 1}
        # base_id: int
        # quote_id: int
        # if isinstance(result, cls._result_cls):
        #     base_id = result.base_external_id
        #     quote_id = result.quote_external_id
        # else:
        #     base_id = result['base']['id']
        #     quote_id = result['quote']['id']
        #
        # base_obj = cls.dbhandlers_router().assets_dbhandler().get_by_external_id(base_id, projection=projection)
        # set_in_dict(result, PAIR_KEYS.BASE_ID, base_obj[MONGODB_ID])
        #
        # quote_obj = cls.dbhandlers_router().assets_dbhandler().get_by_external_id(quote_id, projection=projection)
        # set_in_dict(result, PAIR_KEYS.QUOTE_ID, quote_obj[MONGODB_ID])

        return result

    # @classmethod
    # def get_by_base_asset(cls,
    #                       symbol: str,
    #                       multiple: bool = True,
    #                       **kwargs) -> Union[TResultDict, List[TResultDict]]:
    #     query = {
    #         CryptowatchPriceResult.KEYS.BASE_SYMBOL: symbol
    #     }
    #
    #     result = cls.dbhandlers_router().assets_dbhandler() \
    #         .get(query=query, multiple=multiple, **kwargs)
    #     return result

    @classmethod
    def get_by_exchange_and_pair(cls,
                                 exchange: Union[ObjectId, str, int, TResultDict],
                                 pair: Union[ObjectId, str, int, TResultDict],
                                 min_time: Optional[datetime.datetime] = None,
                                 **kwargs) -> List[TResultDict]:
        query = {}

        if isinstance(exchange, str) and not is_ObjectId(exchange):
            query[PRICE_KEYS.EXCHANGE_SYMBOL] = exchange
        elif is_int(exchange):
            query[PRICE_KEYS.EXCHANGE_EXTERNAL_ID] = exchange
        elif isinstance(exchange, dict):
            query[PRICE_KEYS.EXCHANGE_ID] = to_ObjectId(exchange[MONGODB_ID])
        else:
            query[PRICE_KEYS.EXCHANGE_ID] = to_ObjectId(exchange)

        if isinstance(pair, str) and not is_ObjectId(pair):
            query[PRICE_KEYS.PAIR_SYMBOL] = pair
        elif is_int(pair):
            query[PRICE_KEYS.PAIR_EXTERNAL_ID] = pair
        elif isinstance(pair, dict):
            query[PRICE_KEYS.PAIR_ID] = to_ObjectId(pair[MONGODB_ID])
        else:
            query[PRICE_KEYS.PAIR_ID] = to_ObjectId(pair)

        if isinstance(min_time, (int, float)):
            min_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=min_time)
        elif not isinstance(min_time, datetime.datetime):
            min_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

        query[BaseDbHandler.KEYS.LAST_UPDATE] = {'$gte': min_time}

        kwargs['multiple'] = True
        result = cls.get(query=query, **kwargs)
        return result



