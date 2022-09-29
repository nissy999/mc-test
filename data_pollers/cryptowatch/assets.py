from typing import Dict, Any, List, Optional, Union

from DAL.cryptowatch.assets import AssetsDbHandler
from common.logs.logger import Logger
from common.structs.cryptowatch.assets import CryptowatchAssetResult
from common.structs.results import TResultDict
from data_pollers.bases.api_poller import BaseApiPoller

ASSET_KEYS = CryptowatchAssetResult.KEYS


class CryptowatchAssetsPoller(BaseApiPoller):

    _API_URL = f'{BaseApiPoller._API_URL}/assets'

    _result_cls = CryptowatchAssetResult

    _dbhandler = AssetsDbHandler

    def parse_result(self,
                     result: Union[Dict[str, Any], List[Dict[str, Any]]],
                     url: str,
                     symbol: Optional[str] = None,
                     rdict: bool = False,
                     **kwargs) -> Union[TResultDict, List[TResultDict]]:
        Logger.debug(f'starting to parse result')
        try:
            update = {BaseApiPoller.KEYS.URL: url}
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
    _poller = CryptowatchAssetsPoller()
    try:
        _res = _poller.poll()
        _res2 = _poller.save_result(_res)
    except Exception as ex:
        pass
    print(_res)












