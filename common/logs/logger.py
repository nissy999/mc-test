import logging
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT
import sys
from typing import Optional, Dict, Any, List

from common.consts import APP_NAME
from common.enums.logs import LOG_LEVEL
from common.exceptions.logged import LoggedException


class LogMeta(type):

    def __getattr__(cls, item):
        if LOG_LEVEL.is_key(item.upper()):
            func = getattr(cls.logger(), item.lower())
            return func


class Logger(metaclass=LogMeta):

    _logger: Optional[logging.Logger] = None
    _logger_name: Optional[str] = None
    _formatter: Optional[str] = None

    _DEFAULTS = {
        'level': LOG_LEVEL.DEBUG,
        'handlers': {
            'file': {
                'enabled': True,
                'full_file_path': f'/var/log/{APP_NAME}/{APP_NAME}.log'
            },
            'stdout': {
                'enabled': True
            },
            'stderr': {
                'enabled': True
            }
        },
        'formatter': '%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s',

    }

    @classmethod
    def handlers(cls) -> List[logging.Handler]:
        return cls.logger().handlers

    @classmethod
    def initialize(cls, **kwargs) -> logging.Logger:
        return cls.logger(**kwargs)

    @classmethod
    def logger(cls,
               filepath: Optional[str] = None,
               formatter: Optional[str] = None,
               log_level: Optional[str] = None,  # LOG_LEVEL
               to_stdout: Optional[bool] = None,
               to_stderr: Optional[bool] = None,
               syslog: Optional[Dict[str, Any]] = None,
               **kwargs) -> logging.Logger:
        """
        Returns or initializes a new APPLICATION WIDE logger
        The logger can be extended to support any other type of logging (e.g. SysLog
        :param filepath:
        :param formatter:
        :param log_level:
        :param to_stdout:
        :param to_stderr:
        :param syslog:
        :param kwargs:
        :return:
        """
        if cls._logger:
            return cls._logger

        if not log_level or not LOG_LEVEL.is_value(log_level):
            log_level = cls._DEFAULTS['level']
            print(f'invalid or no log_level was specified, setting it to "{log_level}"')
        if not formatter:
            formatter = cls._DEFAULTS['formatter']
        formatter = logging.Formatter(formatter)
        # separate to formatter per log

        logger_name: str = cls._logger_name if cls._logger_name else __name__
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        def _set_handler(_handler):
            _handler.setLevel(log_level)
            _handler.setFormatter(formatter)
            logger.addHandler(_handler)

        if to_stdout is None:
            to_stdout = ((cls._DEFAULTS.get('handlers') or {}).get('stdout') or {}).get('enabled')
        if to_stdout is True:
            _set_handler(logging.StreamHandler(sys.stdout))
        if to_stderr is None:

            to_stderr = ((cls._DEFAULTS.get('handlers') or {}).get('stderr') or {}).get('enabled')
        if to_stderr is True:
            _set_handler(logging.StreamHandler(sys.stderr))

        if filepath is None:
            log_file_settings: Optional[Dict[str, Any]] = (cls._DEFAULTS.get('handlers') or {}).get('file')
            if log_file_settings and \
                    isinstance(log_file_settings, dict) and \
                    log_file_settings.get('enabled') is True:
                filepath = log_file_settings.get('full_file_path')
        if filepath:
            # validate
            _set_handler(logging.FileHandler(filepath))

        if syslog is None:
            syslog: Optional[Dict[str, Any]] = (cls._DEFAULTS.get('handlers') or {}).get('syslog')
        if syslog and \
                isinstance(syslog, dict) and \
                syslog.get('enabled') is True:
            syslog_host = syslog.get('host')
            syslog_port = syslog.get('port') or SYSLOG_UDP_PORT
            # validate
        else:
            syslog_host = None
            syslog_port = None
        if syslog_host and syslog_port:
            _set_handler(SysLogHandler(address=(syslog_host, syslog_port)))

        cls._logger = logger
        return logger

    @classmethod
    def _raise(cls,
               msg: str,
               ex: Optional[Exception] = None):
        """
        Performs actual exception raising
        :param msg:
        :param ex:
        :return:
        """
        raise LoggedException(msg=msg,
                              correlation_id=ex.correlation_id if isinstance(ex, LoggedException) else None)

    @classmethod
    def critical(cls,
                 msg: str,
                 ex: Optional[Exception] = None,
                 throw: Optional[bool] = False, *args, **kwargs):
        cls.logger().critical(msg, *args, **kwargs)
        if throw:
            cls._raise(msg=msg, ex=ex)

    @classmethod
    def critical_raise(cls,
                       msg: str,
                       ex: Optional[Exception] = None, *args, **kwargs):
        return cls.critical(msg=msg, ex=ex, throw=True)

    @classmethod
    def error(cls,
                 msg: str,
                 ex: Optional[Exception] = None,
                 throw: Optional[bool] = False, *args, **kwargs):
        cls.logger().error(msg, *args, **kwargs)
        if throw:
            cls._raise(msg=msg, ex=ex)

    @classmethod
    def error_raise(cls,
                    msg: str,
                    ex: Optional[Exception] = None, *args, **kwargs):
        return cls.error(msg=msg, ex=ex, throw=True)

    @classmethod
    def exception(cls,
                  msg: str,
                  ex: Optional[Exception] = None,
                  throw: Optional[bool] = False, *args, **kwargs):
        cls.logger().exception(msg, *args, **kwargs)
        if throw:
            cls._raise(msg=msg, ex=ex)

    @classmethod
    def exception_raise(cls,
                        msg: str,
                        ex: Optional[Exception] = None, *args, **kwargs):
        return cls.exception(msg=msg, ex=ex, throw=True)

    @classmethod
    def debug(cls,
              msg: str,
              ex: Optional[Exception] = None,
              throw: Optional[bool] = False, *args, **kwargs):
        cls.logger().debug(msg, *args, **kwargs)
        if throw:
            cls._raise(msg=msg, ex=ex)

    @classmethod
    def debug_raise(cls,
                    msg: str,
                    ex: Optional[Exception] = None, *args, **kwargs):
        return cls.debug(msg=msg, ex=ex, throw=True)
