from typing import Optional, Union, List, Dict

from DAL.bases import BaseDbHandler
from common.structs.cryptowatch.exchanges import CryptowatchExchangeResult
from common.structs.results import TResultDict


EXCHANGE_KEYS = CryptowatchExchangeResult.KEYS


class ExchangesDbHandler(BaseDbHandler):

    _collection_name = 'CryptoWatchExchanges'
    _result_cls = CryptowatchExchangeResult

    _api_to_struct_attributes_mapping: Dict[str, str] = {
        'id': EXCHANGE_KEYS.EXTERNAL_ID,
        'symbol': EXCHANGE_KEYS.SYMBOL,
        'name': EXCHANGE_KEYS.NAME,
        'route': EXCHANGE_KEYS.ROUTE,
        'active': EXCHANGE_KEYS.ACTIVE
    }

    @classmethod
    def get_by_external_id(cls,
                           external_id: Union[int, str],
                           multiple: Optional[bool] = True,
                           **kwargs) -> Optional[Union[TResultDict, List[TResultDict]]]:
        query = {
            EXCHANGE_KEYS.EXTERNAL_ID: int(external_id)
        }
        result = cls.get(query=query, multiple=multiple, **kwargs)
        return result

    @classmethod
    def get_by_symbol(cls,
                      symbol: str,
                      multiple: Optional[bool] = True,
                      **kwargs) -> Optional[Union[TResultDict, List[TResultDict]]]:
        query = {
            EXCHANGE_KEYS.SYMBOL: symbol
        }
        result = cls.get(query=query, multiple=multiple, **kwargs)
        return result


if __name__ == '__main__':
    ff = ExchangesDbHandler.get_by_ids(['63301310d3ae570160d50599', '63301310d3ae570160d50598'])
    print(ff)