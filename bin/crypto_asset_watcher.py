#!/usr/bin/env python3
from typing import List, Dict, Any, Optional

_config = {  # read from file / db
    'assets': {
        'enabled': True,
        'interval': 60 * 60,  # hourly
    },
    'exchanges': {
        'enabled': True,
        'interval': 60 * 60 * 24,
    },
    'pairs': {
        'enabled': True,
        'interval': 60,
    },
    'markets': {
        'enabled': True,
        'interval': 60
    },

    'defaults': {
        'currency': 'btc',
        'interval': 60
    }
}


def main():
    import argparse
    import time

    parser = argparse.ArgumentParser(description='Monte Carlo Test Currency Entrypoint')

    parser.add_argument('-c', '--currency', type=str, help='The currency (symbol) to watch')
    parser.add_argument('-i', '--interval', type=int, help='The interval to run the poller in seconds', default=60)
    parser.add_argument('-e', '--exchange', type=str, help='Optional - The exchange (symbol)')

    args = parser.parse_args()

    currency: str = args.currency if args.currency else _config['defaults']['currency']
    print(f'using "{currency}" as currency')

    interval: int = int(args.interval) if args.interval and args.interval > 0 else _config['defaults']['interval']
    print(f'using "{interval}" as seconds interval')

    from common.structs.cryptowatch.assets import CryptowatchAssetResult as AssetResult
    from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult as PairResult
    from common.structs.cryptowatch.exchanges import CryptowatchExchangeResult as ExchangeResult
    from common.structs.cryptowatch.markets import CryptowatchMarketResult as MarketResult
    from data_pollers.bases.api_poller import BaseApiPoller
    from data_pollers.cryptowatch.utils import CryptoWatchPollersRouter as pollers_router
    from DAL.cryptowatch import CryptoWatchDbHandlersRouter as dbhandlers_router
    from common.structs.cryptowatch.utils import CryptoWatchStructsRouter as structs_router
    from bin.start_poller import start_poller
    from data_pollers.cryptowatch.prices import CryptowatchPricesPoller

    assets_poller: BaseApiPoller = pollers_router.assets()
    # pull all assets - fill and update the db
    # all_assets: List[Dict[str, Any]] = assets_poller.poll(rdict=False)
    # assets_poller.save_result(all_assets, enrich=True)
    # pull all pairs - fill and update the db
    pairs_poller: BaseApiPoller = pollers_router.pairs()
    # all_pairs: List[Dict[str, Any]] = pairs_poller.poll()
    # pairs_poller.save_result(all_pairs, enrich=True)
    # pull all exchanges
    exchanges_poller = pollers_router.exchanges()
    # all_exchanges = exchanges_poller.poll()
    # exchanges_poller.save_result(all_exchanges, enrich=True)

    asset = assets_poller.poll(symbol=currency)
    if not asset:
        raise ValueError(f'could not find the currency "{currency}"')
    markets = asset.get('markets', {})
    if not markets or not markets.get('base'):
        raise ValueError(f'could not find any markets for the currency: "{currency}"')

    # iterate through the different markets of the
    # markets =
    prices_poller = pollers_router.prices()
    for _market in markets['base']:  # type: Dict[str, Any]
        market: MarketResult = dbhandlers_router.markets().parse_to_result(_market, rdict=True)
        market = dbhandlers_router.markets()._enrich(market)

        # pair_symbol: str = _market['pair']
        # exchange_symbol = _market['exchange']

        ff = prices_poller.poll(**{
            CryptowatchPricesPoller.KEYS.EXCHANGE: market.exchange_symbol,
            CryptowatchPricesPoller.KEYS.EXCHANGE_ID: market.exchange_id,
            CryptowatchPricesPoller.KEYS.PAIR: market.pair_symbol,
            CryptowatchPricesPoller.KEYS.PAIR_ID: market.pair_id
        })
        rr = prices_poller.save_to_db(ff)

        # dbhandlers_router.prices().poll(**{CryptowatchPricesPoller.})

        # schedule a poller every one minute
        start_poller(poller='prices', interval=interval, save_to_db=True,
                     poller_kwargs={CryptowatchPricesPoller.KEYS.EXCHANGE: exchange,
                                    CryptowatchPricesPoller.KEYS.PAIR: pair})

    from time import sleep as _sll
    while True:
        _sll(0.3)


if __name__ == '__main__':
    main()
