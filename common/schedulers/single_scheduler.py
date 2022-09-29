import datetime
from typing import Optional, Union, Callable, Iterable, Dict, Any
import pytz
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.schedulers.background import BaseScheduler, BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from common.enums.bases import Enum
from common.utils.strutils import is_int, is_bool


class _KEYS(Enum):
    OBJ = 'obj'
    INTERVAL = 'interval'
    THREADPOOL_SIZE = 'threadpoolSize'
    TIMEZONE = 'timezone'
    START = 'start'


__scheduler__ = {
    _KEYS.OBJ: None,  # type: Optional[BaseScheduler]
    _KEYS.INTERVAL: 60,   # type: Optional[int]    # seconds
    _KEYS.THREADPOOL_SIZE: 1, # 30,
    _KEYS.TIMEZONE: 'UTC',
    _KEYS.START: True
}


def _init_scheduler(threadpool_size: Optional[int] = None,
                    timezone: Optional[Union[datetime.tzinfo, str]] = None,
                    start: Optional[bool] = None,
                    **kwargs) -> BaseScheduler:
    """
    Initializes a scheduler
    :param threadpool_size: optional pool size (threads)
    :param timezone: optional time zone to use
    :param start: indicates wh
    :param kwargs:
    :return:
    """
    if not is_int(threadpool_size) or threadpool_size <= 0:
        threadpool_size = __scheduler__[_KEYS.THREADPOOL_SIZE]
    if not isinstance(timezone, datetime.tzinfo):
        if not timezone:
            timezone = __scheduler__[_KEYS.TIMEZONE]
        timezone = pytz.timezone(timezone)
    if not is_bool(start):
        start = __scheduler__[_KEYS.START]

    _scheduler: BackgroundScheduler = \
        BackgroundScheduler(executors={'default': ThreadPoolExecutor(threadpool_size)},
                            job_defaults={'max_instances': 1},
                            timezone=timezone)
    if start:
        _scheduler.start()
    return _scheduler


def add_job(func: Callable,
            interval: Optional[int] = None,
            next_run_time: Optional[datetime.datetime] = None,
            fargs: Optional[Iterable] = None,
            fkwargs: Optional[Dict[str, Any]] = None,
            **kwargs) -> Job:
    if not is_int(interval) or interval <= 0:
        # handle different cases
        interval = __scheduler__[_KEYS.INTERVAL]
    trigger = IntervalTrigger(seconds=interval)
    kwargs.update({
        'func': func,
        'trigger': trigger
    })
    if fargs:
        kwargs['args'] = fargs
    if fkwargs:
        kwargs['kwargs'] = fkwargs

    kwargs['next_run_time'] = next_run_time if isinstance(next_run_time, datetime.datetime) else \
        datetime.datetime.utcnow() + datetime.timedelta(seconds=0.5)
    result: Job = scheduler().add_job(**kwargs)
    return result


def scheduler(**kwargs) -> BaseScheduler:
    _scheduler: Optional[BaseScheduler] = __scheduler__['obj']
    if not _scheduler:
        _scheduler = __scheduler__['obj'] = _init_scheduler(**kwargs)
    return _scheduler



if __name__ == '__main__':
    from time import sleep as _sl
    from common.logs.logger import Logger as _LL

    def _wwrite(i: int):
        _LL.debug(f'i: {i}')

    _job = add_job(func=_wwrite, interval=1, fkwargs={'i': 22})

    while True:
        _sl(0.5)

