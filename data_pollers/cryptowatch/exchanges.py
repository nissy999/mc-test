from typing import Dict, Any, List

from DAL.cryptowatch.exchanges import ExchangesDbHandler
from common.logs.logger import Logger
from common.structs.cryptowatch.exchanges import CryptowatchExchangeResult
from common.structs.results import TResultDict
from data_pollers.bases.api_poller import BaseApiPoller

EXCHANGE_KEYS = CryptowatchExchangeResult.KEYS


class CryptowatchExchangesPoller(BaseApiPoller):

    _API_URL = f'{BaseApiPoller._API_URL}/exchanges'

    _result_cls = CryptowatchExchangeResult

    _dbhandler = ExchangesDbHandler

    def parse_result(self,
                     result: List[Dict[str, Any]],
                     url: str,
                     rdict: bool = False,
                     **kwargs) -> List[TResultDict]:
        Logger.debug(f'starting to parse result')
        try:
            if rdict:
                result = self._dbhandler.parse_to_result(result) if isinstance(result, dict) else \
                    [self._dbhandler.parse_to_result(_) for _ in result]
                result: List['_result_cls'] = [
                    self._result_cls(**{
                        EXCHANGE_KEYS.EXTERNAL_ID: item['id'],
                        EXCHANGE_KEYS.SYMBOL: item['symbol'],
                        EXCHANGE_KEYS.NAME: item['name'],
                        EXCHANGE_KEYS.ROUTE: item['route'],
                        EXCHANGE_KEYS.ACTIVE: item['active'],
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
    _poller = CryptowatchExchangesPoller()
    try:
        _res = _poller.poll()
        _res2 = _poller.save_result(_res, enrich=True)
    except Exception as ex:
        print(ex)
    print('a')