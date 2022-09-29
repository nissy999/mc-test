from typing import Dict, Any, List

from DAL.cryptowatch.pairs import PairsDbHandler
from common.logs.logger import Logger
from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult
from common.structs.results import TResultDict
from data_pollers.bases.api_poller import BaseApiPoller

PAIRS_KEYS = CryptowatchAssetsPairResult.KEYS


class CryptowatchAssetsPairsPoller(BaseApiPoller):

    _API_URL = 'https://api.cryptowat.ch/pairs'

    _result_cls = CryptowatchAssetsPairResult

    _dbhandler = PairsDbHandler

    def parse_result(self,
                     result: List[Dict[str, Any]],
                     url: str,
                     rdict: bool = False,
                     **kwargs) -> List[TResultDict]:
        Logger.debug(f'starting to parse result')
        try:
            if rdict:
                result: List['_result_cls'] = [
                    self._result_cls(**{
                        PAIRS_KEYS.EXTERNAL_ID: item['id'],
                        PAIRS_KEYS.SYMBOL: item['symbol'],
                        PAIRS_KEYS.ROUTE: item['route'],
                        PAIRS_KEYS.BASE_EXTERNAL_ID: item['base']['id'],
                        PAIRS_KEYS.BASE_SID: item['base']['sid'],
                        PAIRS_KEYS.BASE_SYMBOL: item['base']['symbol'],
                        PAIRS_KEYS.QUOTE_EXTERNAL_ID: item['quote']['id'],
                        PAIRS_KEYS.QUOTE_SID: item['quote']['sid'],
                        PAIRS_KEYS.QUOTE_SYMBOL: item['quote']['symbol'],
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
    _poller = CryptowatchAssetsPairsPoller()
    try:
        _res = _poller.poll()
        _res2 = _poller.save_result(_res, enric)
    except Exception as ex:
        print(ex)
    print('a')