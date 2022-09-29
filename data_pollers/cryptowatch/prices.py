from typing import Dict, Any, List, Optional, Union

from bson import ObjectId

from DAL.cryptowatch.pairs import PairsDbHandler
from common.enums.bases import Enum
from common.logs.logger import Logger
from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult
from common.structs.results import TResultDict
from common.utils.strutils import to_ObjectId
from data_pollers.bases.api_poller import BaseApiPoller

PAIRS_KEYS = CryptowatchAssetsPairResult.KEYS


class CryptowatchPricesPoller(BaseApiPoller):

    _API_URL = 'https://api.cryptowat.ch/markets/{exchange}/{pair}/price'

    _result_cls = CryptowatchAssetsPairResult

    _dbhandler = PairsDbHandler

    class KEYS(Enum):
        EXCHANGE = 'exchange_symbol'
        PAIR = 'pair_symbol'

        EXCHANGE_ID = 'exchange_id'
        PAIR_ID = 'pair_id'

    def _url_symbol_dict(self,
                         exchange_symbol: str,
                         pair_symbol: str,
                         exchange_id: Optional[Union[str, ObjectId]] = None,
                         pair_id: Optional[Union[str, ObjectId]] = None,
                         **kwargs) -> Dict[str, Any]:
        result = {
            BaseApiPoller.KEYS.URL: self._API_URL.format(exchange=exchange_symbol, pair=pair_symbol),
            self.KEYS.EXCHANGE: exchange_symbol,
            self.KEYS.PAIR: pair_symbol,
        }
        if exchange_id:
            result[self.KEYS.EXCHANGE_ID] = to_ObjectId(exchange_id)
        if pair_id:
            result[self.KEYS.PAIR_ID] = to_ObjectId(pair_id)
        return result

    def parse_result(self,
                     result: List[Dict[str, Any]],
                     rdict: bool = False,
                     **kwargs) -> List[TResultDict]:
        Logger.debug(f'starting to parse result')
        try:
            update = self._url_symbol_dict(**kwargs)
            # change underscore
            if rdict:
                result = self._dbhandler.parse_to_result(result) if isinstance(result, dict) else \
                    [self._dbhandler.parse_to_result(_) for _ in result]
            elif isinstance(result, dict):
                result.update(update)
            else:
                [_.update(update) for _ in result]

            return result
        finally:
            Logger.debug(f'finished parsing result')


if __name__ == '__main__':
    _poller = CryptowatchPricesPoller()
    rr = _poller.poll(pair_symbol='btcusd', exchange_symbol='bitfinex')
    _poller.save_result(rr, enrich=True)
    try:
        _res = _poller.poll()
        _res2 = _poller.save_result(_res, enric)
    except Exception as ex:
        print(ex)
    print('a')