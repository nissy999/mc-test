import datetime
from typing import Optional, Union, Dict, Any, List

from bson import ObjectId

from DAL.bases import BaseDbHandler
from common.consts import MONGODB_ID
from common.structs.cryptowatch.assets import CryptowatchAssetResult
from common.structs.cryptowatch.markets import CryptowatchMarketResult
from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult
from common.structs.cryptowatch.exchanges import CryptowatchExchangeResult
from common.structs.results import TResultDict
from common.utils.collectionsutils import get_from_dict, set_in_dict

MARKET_KEYS = CryptowatchMarketResult.KEYS
PAIR_KEYS = CryptowatchAssetsPairResult.KEYS
EXCHANGE_KEYS = CryptowatchExchangeResult.KEYS


class MarketsDbHandler(BaseDbHandler):

    _collection_name = 'CryptoWatchMarkets'
    _result_cls = CryptowatchMarketResult

    _api_to_struct_attributes_mapping = {
        'id': MARKET_KEYS.EXTERNAL_ID,
        'active': MARKET_KEYS.ACTIVE,
        'exchange': MARKET_KEYS.EXCHANGE_SYMBOL,
        'pair': MARKET_KEYS.PAIR_SYMBOL,
        'route': MARKET_KEYS.ROUTE
    }

    @classmethod
    def _enrich(cls,
                result: TResultDict,
                now: Optional[datetime.datetime] = None,
                date_added: Optional[Union[bool, datetime.datetime]] = None,
                last_update: Optional[Union[bool, datetime.datetime]] = None,
                add_item: Optional[bool] = None,
                **kwargs):
        result = super()._enrich(result=result, now=now, date_added=date_added, last_update=last_update)

        exchange_symbol: Optional[str] = get_from_dict(result, MARKET_KEYS.EXCHANGE_SYMBOL)
        exchange: Optional[CryptowatchExchangeResult] = \
            cls.dbhandlers_router().exchanges().get_by_symbol(exchange_symbol, multiple=False, rdict=True) \
            if exchange_symbol else None
        if exchange:
            # create update in dict
            set_in_dict(result, key=MARKET_KEYS.EXCHANGE_ID, value=exchange[MONGODB_ID])
            set_in_dict(result, key=MARKET_KEYS.EXCHANGE_EXTERNAL_ID, value=exchange.external_id)

        pair_symbol: Optional[str] = result.get(MARKET_KEYS.PAIR_SYMBOL)
        pair: Optional[CryptowatchAssetsPairResult] = \
            cls.dbhandlers_router().pairs().get_by_symbol(pair_symbol, multiple=False, rdict=True) \
            if pair_symbol else None
        if pair:
            set_in_dict(result, key=MARKET_KEYS.PAIR_ID, value=pair[MONGODB_ID])
            set_in_dict(result, key=MARKET_KEYS.PAIR_EXTERNAL_ID, value=pair.external_id)

        return result

    @classmethod
    def get_by_base_asset(cls,
                          symbol: str,
                          multiple: bool = True,
                          **kwargs) -> List[TResultDict]:
        markets: CryptowatchMarketResult
        query = {
            CryptowatchMarketResult.KEYS.PAIR_SYMBOL: symbol
        }

        result = cls.dbhandlers_router().assets().get(query=query, multiple=multiple, **kwargs)
        return result


