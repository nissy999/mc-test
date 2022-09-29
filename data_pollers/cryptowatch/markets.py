from typing import Dict, Any, List, Union, Optional, Callable

from DAL.cryptowatch.markets import MarketsDbHandler
from DAL.interfaces import IBaseDbHandler
from common.logs.logger import Logger
from common.structs.cryptowatch.assets import CryptowatchAssetResult
from common.structs.cryptowatch.markets import CryptowatchMarketResult
from common.structs.results import TResultDict
from common.utils.strutils import is_int
from data_pollers.bases.api_poller import BaseApiPoller

MARKET_KEYS = CryptowatchMarketResult.KEYS


class CryptowatchMarketsPoller(BaseApiPoller):

    _API_URL = 'https://api.cryptowat.ch/markets'

    _result_cls = CryptowatchMarketResult

    _dbhandler = MarketsDbHandler

    def parse_result(self,
                     result: List[Dict[str, Any]],
                     url: str,
                     symbol: Optional[str] = None,
                     rdict: bool = False,
                     **kwargs) -> List[TResultDict]:
        Logger.debug(f'starting to parse result')
        try:
            if rdict:
                result: List['_result_cls'] = [
                    self._result_cls(**{
                        MARKET_KEYS.EXTERNAL_ID: item['id'],
                        MARKET_KEYS.EXCHANGE_SYMBOL: item['exchange'],
                        MARKET_KEYS.PAIR_SYMBOL: item['pair'],
                        MARKET_KEYS.ACTIVE: item['active'],
                        MARKET_KEYS.ROUTE: item['route'],
                        self.KEYS.URL: url
                    }) for item in result
                ]
            else:
                update = {self.KEYS.URL: url}
                [_.update(update) for _ in result]

            return result
        finally:
            Logger.debug(f'finished parsing result')


if __name__ == '__main__':
    _poller = CryptowatchAssetsPoller()
    try:
        _res = _poller.poll()
        _res2 = _poller.save_result(_res)
    except Exception as ex:
        pass
    print(_res)












