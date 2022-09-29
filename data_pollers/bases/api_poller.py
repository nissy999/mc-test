from abc import ABC
from typing import Dict, Any, List, Callable, Optional, Union, Iterable

import requests

from DAL.bases import BaseDbHandler
from common.enums.bases import Enum
from common.logs.logger import Logger
from common.structs.results import TResultDict
from data_pollers.bases import BaseDataPoller


class BaseApiPoller(BaseDataPoller, ABC):

    _API_URL: str = 'https://api.cryptowat.ch'

    # __PARAMS_KEY__ = ''.join([str(uuid.uuid4()) for _ in range(2)])
    # pass parameters as an object (dict is sufficient) holding references to common params such as url (primitive types)

    class KEYS(Enum):
        URL = 'url'
        SYMBOL = 'symbol'

    @classmethod
    def api_url(cls,
                symbol: Optional[str] = None,
                **kwargs) -> str:
        """
        Generates the API URL to use taking into account an optional symbol
        :param symbol:
        :param kwargs:
        :return:
        """
        parts = [cls._API_URL.rstrip(' /')]
        if symbol:
            parts.append(symbol)
        return '/'.join(parts)

    # region poll

    def _url_symbol_dict(self,
                         symbol: Optional[str] = None,
                         **kwargs) -> Dict[str, Any]:
        # helper method
        result = {
            BaseApiPoller.KEYS.URL: self.api_url(symbol=symbol)
        }
        if symbol:
            result[BaseApiPoller.KEYS.SYMBOL] = symbol
        return result

    def _generate_parse_result_params(self,
                                      result: Union[TResultDict, List[TResultDict]],
                                      symbol: Optional[str] = None,
                                      **kwargs) -> Dict[str, Any]:
        params: Dict[str, Any] = super()._generate_poll_parameters(**kwargs)
        params.update(self._url_symbol_dict(symbol=symbol, **kwargs))
        return params

    def _generate_poll_parameters(self,
                                  symbol: Optional[str] = None,
                                  **kwargs) -> Dict[str, Any]:
        params: Dict[str, Any] = super()._generate_poll_parameters(**kwargs)
        params.update(self._url_symbol_dict(symbol=symbol, **kwargs))
        return params

    def _poll(self,
              url: str,
              rdict: bool = False,
              symbol: Optional[str] = None,
              **kwargs) -> List[TResultDict]:
        http_method = 'GET'  # get as param
        Logger.debug(f'starting to poll from "{url}"')
        success: bool = True
        try:
            try:
                func: Callable[[str, Optional[Dict[str, Any]]], requests.models.Response] = \
                    getattr(requests, http_method.lower())
                response: requests.models.Response = func(url)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to poll from "{url}" - ex: "{str(ex)}')

            Logger.debug(f'api request successful - status code: "{response.status_code}"')

            kwargs.update({
                BaseApiPoller.KEYS.URL: url,
                BaseApiPoller.KEYS.SYMBOL: symbol,
                self._RDICT_PARAM_NAME: rdict
            })
            try:
                params: Dict[str, Any] = self._generate_parse_api_response_parameters(**kwargs)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to generate parse api response parameters - ex: "{str(ex)}"')

            if isinstance(params, dict) and params:
                kwargs.update(params)
            try:
                result: List[TResultDict] = self.parse_api_response(response=response, **kwargs)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to parse api response - ex: "{str(ex)}"')

            Logger.debug('finished polling data from api - url: "{url}" - success: "{success}" - '
                         f'num results: "{len(result)}"')
            return result

        finally:
            Logger.debug(f'finished polling from "{url}" - success: "{success}")')

    def parse_result(self,
                     result: List[TResultDict],
                     url: str,
                     rdict: bool = False,
                     **kwargs) -> List[TResultDict]:
        Logger.debug(f'starting to parse result from "{url}"')
        try:
            try:
                try:
                    params: Dict[str, Any] = self._generate_parse_api_response_parameters(**kwargs)
                except Exception as ex:
                    success = False
                    Logger.exception_raise(f'failed to generate parse api response parameters - ex: "{str(ex)}"')

                if isinstance(params, dict) and params:
                    kwargs.update(params)
                try:
                    result: List[TResultDict] = self.parse_api_response(response=response, **kwargs)
                except Exception as ex:
                    success = False
                    Logger.exception_raise(f'failed to parse api response - ex: "{str(ex)}"')

                Logger.debug('finished polling data from api - url: "{url}" - success: "{success}" - '
                             f'num results: "{len(result)}"')
                return result
            except TypeError:
                pass
        finally:
            pass

    def parse_api_response(self,
                           response: requests.models.Response,
                           url: str,
                           rdict: bool = False,
                           set_url: bool = False,
                           **kwargs) -> List[TResultDict]:
        Logger.debug(f'starting to parse polled data - url: "{url}" - rdict: "{rdict}"')

        success = True
        try:
            try:
                data: Dict[str, Any] = response.json()
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to get response json - ex: "{str(ex)}"')

            # validation

            result: Optional[List[Dict[str, Any]]] = data.get('result')
            if not result:
                Logger.debug('no results were found')
                return []
            return result
        finally:
            Logger.debug(f'finished parsing polled data - success: "{success}"')

    # endregion poll

    #region api response

    def _generate_parse_api_response_parameters(self,
                                                symbol: Optional[str] = None,
                                                **kwargs) -> Dict[str, Any]:
        params: Dict[str, Any] = super()._generate_poll_parameters(**kwargs)
        params.update(self._url_symbol_dict(symbol=symbol, **kwargs))
        return params

    # endregion api response

    def start(self,
              save_to_db: bool,
              interval: Optional[int] = None,
              fargs: Optional[Iterable] = None,
              fkwargs: Optional[Dict[str, Any]] = None,
              **kwargs):
        from common.schedulers.single_scheduler import add_job
        if save_to_db:
            def _func(*_args, **_kwargs):
                result = self.poll(*_args, **_kwargs)
                return self.save_result(result=result, **_kwargs)
        else:
            _func = self.poll
        job = add_job(func=_func, interval=interval, args=fargs, kwargs=fkwargs, **kwargs)

    #region db

    _dbhandler: BaseDbHandler = None

    def save_result(self,
                    result: List[TResultDict],
                    enrich: Optional[bool] = True,
                    **kwargs) -> Union[TResultDict, List[TResultDict]]:
        Logger.debug(f'starting to save {len(result)} results to the db')
        success = True
        try:
            try:
                result = self._dbhandler.save_to_db(result=result, enrich=enrich, **kwargs)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to save result to db - ex: "{str(ex)}"')

            return result
        finally:
            Logger.debug(f'finished saving {len(result)} results to the db - success: {success}')

    # endregion db
