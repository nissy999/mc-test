import datetime
from typing import Any, Optional, Tuple

__FORMATS__ = {
    'milliseconds': f'%Y-%m-%d %H:%M:%S.%f'
}


def strftime_milliseconds(dt: datetime.datetime) -> str:
    return dt.strftime(__FORMATS__['milliseconds'])


def are_dates_and_elapsed_aligned(start_time: datetime.datetime,
                                  end_time: datetime.datetime,
                                  elapsed: float,
                                  throw: Optional[bool] = True):
    """
    Check if the difference between two datetime objects total milliseconds equals to the elapsed milliseconds
    :param start_time:
    :param end_time:
    :param elapsed:
    :return:
    """

    if not is_datetime(start_time):
        _logger_error(f'start_time is of invalid type: "{type(start_time)}"')
        return False
    if not is_datetime(end_time):
        _logger_error(f'end_time is of invalid type: "{type(end_time)}"')
        return False
    if end_time < start_time:
        _logger_error(f'end_time is not greater than start_time - '
                      f'start_time: "{strftime_milliseconds(start_time)}" - '
                      f'end_time: "{strftime_milliseconds(end_time)}"')
        return False

    dates_diff: float = round((end_time.timestamp() - start_time.timestamp()) * 1000)  # microseconds
    elapsed = round(elapsed)
    if dates_diff != elapsed:
        _logger_error(f'end_time - start_time diff is different than elapsed - '
                      f'elapsed: "{elapsed}" - '
                      f'start_time: "{strftime_milliseconds(start_time)}" - '
                      f'end_time: "{strftime_milliseconds(end_time)}"')

    return True


def is_datetime(dt: Any) -> bool:
    """
    Check if a variable is a valid datetime.datetime object
    """
    return isinstance(dt, datetime.datetime)


def parse_time_and_elapsed(elapsed: Optional[float] = None,  # elapsed time milliseconds
                           start_time: datetime.datetime = None,
                           end_time: datetime.datetime = None) -> \
        Tuple[float, datetime.datetime, datetime.datetime]:
    if elapsed is not None:
        if is_datetime(start_time) and not is_datetime(end_time):
            end_time = start_time + datetime.timedelta(milliseconds=elapsed)
        elif is_datetime(end_time) and not is_datetime(start_time):
            start_time = end_time - datetime.timedelta(milliseconds=elapsed)

    else:
        if is_datetime(start_time) and not is_datetime(end_time):
            _logger_error('neither end_time nor elapsed were specified')
        elif not is_datetime(start_time):
            # elapsed and end_time are None
            _logger_error('neither start_time nor elapsed were specified')
        elapsed = round((end_time.timestamp() - start_time.timestamp()) * 1000.0)

    return elapsed, start_time, end_time


def _logger_error(msg: str,
                  throw: Optional[bool] = True):
    from common.logs.logger import Logger as _logger_
    _logger_.error(msg=msg, throw=throw)
