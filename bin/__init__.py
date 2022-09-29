from typing import Dict, Optional, Any
import sys
from pathlib import Path

POLLERS_MAPPING: Dict[str, str] = {
    'assets': 'CryptowatchAssetsPoller',
    'exchanges': 'CryptowatchExchangesPoller',
    'markets': 'CryptowatchMarketsPoller',
    'pairs': 'CryptowatchAssetsPairsPoller',
    'prices': 'CryptowatchPricesPoller',
}

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

