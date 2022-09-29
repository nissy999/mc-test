#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from . import POLLERS_MAPPING


def start_poller(poller: str,
                 interval: int,
                 save_to_db: bool,
                 poller_kwargs: Optional[Dict[str, Any]] = None):
    path = Path(__file__)
    parent_path = str(path.parent.absolute())
    expected_path = str(path.parent.parent.absolute())
    if expected_path not in sys.path:
        sys.path.insert(0, expected_path)
    if parent_path in sys.path:
        sys.path.remove(parent_path)

    expected_class = POLLERS_MAPPING[poller]

    import importlib
    mdl = importlib.import_module(f'data_pollers.cryptowatch.{poller}')

    worker_cls = next((getattr(mdl, _)
                       for _ in dir(mdl)
                       if str(_) == expected_class), None)
    if not worker_cls:
        raise ValueError(f'could not resolve starting point, program: "{poller}"')

    worker = worker_cls()
    job = worker.start(interval=interval, save_to_db=save_to_db, **(poller_kwargs or {}))
    return job


def main():
    parser = argparse.ArgumentParser(description='Monte Carlo Test Poller Entrypoint')

    parser.add_argument('-p', '--poller', type=str, help='The poller to start: assets/exchanges/markets/pairs',
                        default='pairs')
    parser.add_argument('-i', '--interval', type=int, help='The interval to run the poller in seconds', default=60)
    parser.add_argument('-d', '--db', type=bool, help='Indicates whether to save results in the db', default=True)

    args = parser.parse_args()

    poller: str = args.poller
    if poller not in POLLERS_MAPPING:
        raise ValueError(f'invalid poller: "{str(poller)}"')

    start_poller(poller=poller, interval=args.interval, save_to_db=args.db)

    # for poller in ('assets',  'exchanges', 'markets', 'pairs'):
    #     start_poller(poller=poller, interval=args.interval, save_to_db=args.db)

    import time as _time
    while True:
        _time.sleep(0.5)


if __name__ == '__main__':
    main()
