import datetime
from typing import Optional, List

from flask import Blueprint

from DAL.cryptowatch.assets import AssetsDbHandler
from DAL.cryptowatch.pairs import PairsDbHandler
from DAL.cryptowatch.prices import PricesDbHandler
from common.consts import MONGODB_ID
from common.logs.logger import Logger
from common.structs.cryptowatch.assets import CryptowatchAssetResult
from common.structs.cryptowatch.pairs import CryptowatchAssetsPairResult
from common.utils.jsonutils import JsonEncoderJS
from rest_api.utils.flaskutils import raise_bad_request

_blueprint_name = __name__.split('.')[-1]
blueprint = Blueprint('{}_app'.format(_blueprint_name), __name__)


@blueprint.route('/quotes/<string:base_symbol>/<string:quote_symbol>/<string:from_time>')
def get_quotes_from_ts(base_symbol: str,
                       quote_symbol: str,
                       from_time: str):
    # authentication and authorization

    # validation
    base_asset: Optional[CryptowatchAssetResult] = \
        AssetsDbHandler.get_by_external_id(base_symbol, multiple=False, rdict=True)
    if not base_asset:
        error = f'invalid base_asset: "{base_asset}"'
        Logger.error(error)
        return raise_bad_request(error)
    quote_asset: Optional[CryptowatchAssetResult] = \
        AssetsDbHandler.get_by_external_id(quote_symbol, multiple=False, rdict=True)
    if not quote_asset:
        error = f'invalid base_asset: "{quote_asset}"'
        Logger.error(error)
        return raise_bad_request(error)

    start_time: datetime.datetime.strptime(from_time, '%Y-%m-%d-%H:%M')

    pairs: List[CryptowatchAssetsPairResult] = PairsDbHandler.get_by_base_asset(symbol=base_asset.symbol,
                                                                                quote_symbol=quote_asset.symbol,
                                                                                rdict=True, multiple=True)
    pairs_by_symbols = {_[CryptowatchAssetsPairResult.KEYS.SYMBOL]: _ for _ in pairs}

    quotes: List = []
    for pair in pairs:
        markets = [_ for _ in base_asset['markets']['base'] if _['pair'] == pair.symbol]

        for market in markets:
            market_prices = PricesDbHandler.get_by_exchange_and_pair(exchange=market['exchange'],
                                                                     pair=pair,
                                                                     min_time=start_time)
            quotes.append(market_prices)

    return JsonEncoderJS.json_encode(quotes)

@blueprint.route('/quotes/<string:base_symbol>/<string:quote_symbol>')
def get_quotes(base_symbol: str,
               quote_symbol: str):

    pairs: List[CryptowatchAssetsPairResult] = PairsDbHandler.get_by_base_asset(symbol=base_asset.symbol,
                                                                                quote_symbol=quote_asset.symbol,
                                                                                rdict=True, multiple=True)
    pairs_by_symbols = {_[CryptowatchAssetsPairResult.KEYS.SYMBOL]: _ for _ in pairs}

    quotes: List = []
    for pair in pairs:
        markets = [_ for _ in base_asset['markets']['base'] if _['pair'] == pair.symbol]

        for market in markets:
            market_prices = PricesDbHandler.get_by_exchange_and_pair(exchange=market['exchange'],
                                                                     pair=pair)
            quotes.append(market_prices)

    return JsonEncoderJS.json_encode(quotes)



# for load balancers
@blueprint.route('/helthchk', methods=['HEAD'])
def _healthcheck(*args, **kwargs):
    return "OK"