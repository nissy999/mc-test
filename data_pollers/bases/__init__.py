import copy
from abc import ABC, abstractmethod
from typing import Type, Dict, Any, Union, List, Optional, Iterable

from common.consts import LIST_TYPES
from common.logs.logger import Logger
from common.structs.results import TResultDict
from common.utils.strutils import is_bool


class BaseDataPoller(ABC):

    _result_cls: Type[TResultDict] = None

    _rdict: bool = False
    _RDICT_PARAM_NAME: str = 'rdict'

    @classmethod
    def RDICT_PARAM_DICT(cls,
                         rdict: bool = None,
                         **kwargs) -> Dict[str, Any]:
        if not is_bool(rdict):
            rdict = cls._rdict
        return {
            cls._RDICT_PARAM_NAME: rdict
        }

    # region poll

    def poll(self, **kwargs) -> Union[TResultDict, List[TResultDict]]:
        Logger.debug('starting iteration')
        success: bool = True
        try:
            try:
                poll_params: Dict[str, Any] = self._generate_poll_parameters(**kwargs)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to generate poll parameters: "{str(ex)}"', ex=ex)

            params = copy.deepcopy(kwargs)
            params.update(poll_params)
            Logger.debug(f'total of {len(params)} were generated - {",".join(list(params.keys()))}')
            try:
                result: Union[TResultDict, List[TResultDict]] = self._poll(**params)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to poll - ex: {str(ex)}', ex=ex)

            def _len(_result: Union[TResultDict, List[TResultDict]]) -> int:
                return len(_result) if isinstance(_result, LIST_TYPES) else 1

            Logger.debug(f'got a total of {_len(result)} results - starting to parse results')
            try:
                parse_params: Dict[str, Any] = self._generate_parse_result_params(result=result, **kwargs)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to generate parse result parameters - ex: "{str(ex)}"', ex=ex)

            params = copy.deepcopy(kwargs)
            params.update(parse_params)
            try:
                parsed_result: Union[TResultDict, List[TResultDict]] = self.parse_result(result=result, **params)
            except Exception as ex:
                success = False
                Logger.exception_raise(f'failed to parse result - ex: "{str(ex)}"', ex=ex)

            Logger.debug(f'finished parsing result - got {_len(result)} result')

            return parsed_result
        finally:
            Logger.debug(f'finished iteration - status: "{success}"')

    def _generate_poll_parameters(self,
                                  rdict: bool = None,
                                  **kwargs) -> Dict[str, Any]:
        return self.RDICT_PARAM_DICT(rdict, **kwargs)

    @abstractmethod
    def _poll(self,
              symbol: Optional[str] = None,
              rdict: bool = False,
              **kwargs) -> Union[TResultDict, List[TResultDict]]:
        """
        Performs the actual data polling operation
        :param kwargs: should contain all relevant parameters
        :param rdict: indicates whether to transform the result to struct
        :param symbol: optional symbol to use
        :return:
        """
        raise NotImplementedError()

    # endregion poll

    # region parse result

    def _generate_parse_result_params(self,
                                      result: Union[TResultDict, List[TResultDict]],
                                      **kwargs) -> Dict[str, Any]:
        return kwargs

    @abstractmethod
    def parse_result(self,
                     result: Union[TResultDict, List[TResultDict]],
                     **kwargs) -> Union[TResultDict, List[TResultDict]]:
        raise NotImplementedError()

    # endregion parse result

    def __call__(self, **kwargs):
        return self.poll(**kwargs)

    # region db

    @abstractmethod
    def save_result(self,
                    result: Union[TResultDict, List[TResultDict]],
                    **kwargs) -> Union[TResultDict, List[TResultDict]]:
        raise NotImplementedError()

    # endregion db
