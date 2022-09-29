# Monte Carlo Test

This repo contains the home assignment code for Monte Carlo.

The cryptocurrencies data is pulled from [Cryptowatch API](https://cryptowat.ch/docs/api).

There are several entrypoints and several ways to run the pollers / api as specified below

```TResultDict``` is a TypeVar definition used throughout the project to describe an item which 
may be a ```Dict[str, Any]``` or a ```BaseResult``` (see below)

```python
TResult = TypeVar('TResult', bound=BaseResult)

TResultDict = TypeVar('TResultDict', bound=Union[BaseResult, Dict[str, Any]])
```


## Table of content

- [Installation](#installation)
- [Data Pollers](#Data Pollers)
    - [Pollers Inheritance](#Pollers Inheritance)
    - [Pollers List](#Pollers List)
    - [Poller Usage](#Poller Usage)
- [Data Structs](#Data Structs)
    - [Data Structs Inheritance](#Data Structs Inheritance)
    - [Data Structs List](#Data Structs List)
- [DB Handlers](#DB Handlers)
- [Assignment Tasks](#Assignment Tasks)
    - [Periodic Polling](#Periodic Polling)
    - [Flask API](#Flask API)
  

## Installation

* Clone the repo
```bash
git clone https://github.com/nissy999/mc-test
```
* Create a virtualenv
```bash
python3.8 -m virtualenv venv
```
* Install the requirements
```bash
venv/bin/pip install -r requirements.txt
```

## Data Pollers

All the data pollers can be found in the [data_pollers/cryptowatch](nissy999/mc-test/blob/master/data_pollers/cryptowatch) folder

Each poller is responsible for a single "poll" operation

### Pollers Inheritance

Each data poller inherits from [BaseApiPoller](nissy999/mc-test/blob/master/data_pollers/bases/api_poller.py) 
which in term inherits from [BaseDataPoller](nissy999/mc-test/blob/master/data_pollers/bases/__init__.py)

BaseApiPoller allows querying a specific item using the `symbol` parameter

### Pollers List

The available pollers are:
* Assets - [CryptowatchAssetsPoller](nissy999/mc-test/blob/master/data_pollers/cryptowatch/assets.py)
* Exchanges - [CryptowatchExchangesPoller](nissy999/mc-test/blob/master/data_pollers/cryptowatch/exchanges.py)
* Pairs - [CryptowatchAssetsPairsPoller](nissy999/mc-test/blob/master/data_pollers/cryptowatch/pairs.py)
* Markets - [CryptowatchMarketsPoller](nissy999/mc-test/blob/master/data_pollers/cryptowatch/markets.py)

### Poller Usage

A poller has 2 main method it exposes

* Polling data from the API 
```python
# BaseDataPoller
def poll(self, **kwargs) -> Union[TResultDict, List[TResultDict]]:

# BaseApiPoller
def poll(self, 
         symbol: Optional[str] = None,
         **kwargs) -> Union[TResultDict, List[TResultDict]]:
```
* Saving the polled data to the database
```python
# BaseDataPoller
def save_result(self,
                result: Union[TResultDict, List[TResultDict]],
                **kwargs) -> Union[TResultDict, List[TResultDict]]:

# BaseApiPoller
def save_result(self,
                result: Union[TResultDict, List[TResultDict]],
                symbol: Optional[str] = None,
                **kwargs) -> Union[TResultDict, List[TResultDict]]:

```

## Data Structs

Data Structs are saved in the 
[common/structs/cryptowatch](nissy999/mc-test/blob/master/common/structs/cryptowatch) folder

### Data Structs Inheritance

* Each data structs inherits from [BaseResult](nissy999/mc-test/blob/master/common/structs/results.py).
* ``BaseResult`` inherits from [BaseStruct](nissy999/mc-test/blob/master/common/structs/bases.py) 
which exposes the ```_set``` method which allows to manipulate attributes easily
```python
def _set(self,
         key: str,
         value: Optional[Any] = None,
         pop: Optional[bool] = None,
         validate: Optional[Callable[[Any], Any]] = None,
         trans: Optional[Callable[[Any], Any]] = None,
         reset: Optional[str] = None,
         **kwargs):
"""
Sets or removes an attribute from the object's dict.
Supports nested attributes (dot notation)
:param key: the key to set/remove
:param value: the value to set/remove
:param pop: indicates whether to remove the key if the value is None
:param validate: an optional callable which validates the value
:param trans: an optional callable which transforms the value to another scalar value
:param reset: an options string representing an attribute of the current object which value should be reseted
:param kwargs:
:return:
"""
```
* ```BaseStruct``` inherits from [RDict](nissy999/mc-test/blob/master/common/utils/collectionsutils.py) 
which is a dict allowing dot notation ```get``` calls and a new ```set``` method
```python
def set(self,
        key: str,
        value: Optional[Any] = None):
```
Recursive lookup is also exposed by external methods (didn't have to time to combine) 
```python
def get_from_dict(dct: Dict[str, Any],
                  key: Any,
                  default: Optional[Any] = None) -> Optional[Any]:

def set_in_dict(dct: Dict[str, Any],
                key: str,
                value: Optional[Any] = None):
    
```

### Data Structs List

The available pollers are:
* Assets - [CryptowatchAssetResult](nissy999/mc-test/blob/master/common/structs/cryptowatch/assets.py)
* Exchanges - [CryptowatchExchangeResult](nissy999/mc-test/blob/master/common/structs/cryptowatch/exchanges.py)
* Pairs - [CryptowatchAssetsPairResult](nissy999/mc-test/blob/master/common/structs/cryptowatch/pairs.py)
* Markets - [CryptowatchMarketResult](nissy999/mc-test/blob/master/common/structs/cryptowatch/markets.py)


## DB Handlers

Although not specified in the instruction in order to show progress over time I've 
implemented a thin layer of DAL (Database Access Layer) in [DAL/cryptowatch](nissy999/mc-test/blob/master/DAL/cryptowatch)

I've used mongodb for simplicity of implementation - I've added the ```MONGODB_ID``` attribute to allow 
RDBMS constraints as well. 
The foreign keys are added when calling the ```_enrich``` method for poller result  

The implementation consists of a handler for each collection. I've used classmethods for simplicity and speed of 
development. For ease of access to the different handlers I've built a "router"
([CryptoWatchDbHandlersRouter](nissy999/mc-test/blob/master/DAL/cryptowatch/__init__.py)) 
holding a single reference to each of 
the handlers upon first call (late binding)  

The main methods exposed by each handler are:

```python
@classmethod
def save_to_db(cls,
               result: Union[TResultDict, List[TResultDict]],
               enrich: bool = True,
               now: Optional[datetime.datetime] = None,
               date_added: Optional[Union[bool, datetime.datetime]] = None,
               last_update: Optional[Union[bool, datetime.datetime]] = None,
               **kwargs) -> Union[TResultDict, List[TResultDict]]:

@classmethod
def get(cls,
        query: Dict[str, Any],
        multiple: bool = True,
        cursor: bool = False,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        rdict: bool = False,
        **kwargs) -> Optional[Union[TResultDict, List[TResultDict]]]:

@classmethod
def get_by_id(cls,
              id_: TID,
              **kwargs) -> Optional[TResultDict]:

@classmethod
def get_by_ids(cls,
               ids: Union[TID, TIDS],
               **kwargs) -> List[TResultDict]:
  
@classmethod
def _enrich(cls,
            result: TResultDict,
            now: Optional[datetime.datetime] = None,
            date_added: Optional[Union[bool, datetime.datetime]] = None,
            last_update: Optional[Union[bool, datetime.datetime]] = None,
            **kwargs) -> TResultDict:

```

## Assignment Tasks

### Periodic Polling

In order to pull the latest quotes for a specific currency we can use the [bin/crypto_asset_watcher.py](nissy999/mc-test/blob/master/bin/crypto_asset_watcher.py) 

The logic is as following (using "btc" as curreny):
1. Pull the asset markets data based on the currency symbol ```https://api.cryptowat.ch/assets/btc```
The result contains the different exchange+pairs to track
```json
{
  "markets": {
    "base": [
      {
        "id": 1,
        "exchange": "bitfinex",
        "pair": "btcusd",
        "active": true,
        "route": "https://api.cryptowat.ch/markets/bitfinex/btcusd"
      },
      {
        "id": 65,
        "exchange": "coinbase-pro",
        "pair": "btcusd",
        "active": true,
        "route": "https://api.cryptowat.ch/markets/coinbase-pro/btcusd"
      }, ...
    ],
    "quote": [
      {
          "id": 3,
          "exchange": "bitfinex",
          "pair": "ltcbtc",
          "active": true,
          "route": "https://api.cryptowat.ch/markets/bitfinex/ltcbtc"
        },
        {
          "id": 5,
          "exchange": "bitfinex",
          "pair": "ethbtc",
          "active": true,
          "route": "https://api.cryptowat.ch/markets/bitfinex/ethbtc"
        }, ...
    ]
  }
}
```

2. Schedule the [CryptowatchPricesPoller](nissy999/mc-test/blob/master/data_pollers/cryptowatch/prices.py) to run periodically - every 1 minute.
If using apscheduler (not recommended) you can use [bin/start_poller.py](nissy999/mc-test/blob/master/data_pollers/cryptowatch/prices.py).

Scheduling using AWS Scheduled Lambda by creating scheduled events is a better solution. 
The poller can also be implemented to read currencies continuously from a queue (SQS/kafka etc.) and stop
the lambda execution only after no more currencies are available

The poller must accept 2 sets of arguments:

```exchange_symbol``` and ```exchange_id``` - representing the required exchange (mandatory)

```pair_symbol``` and ```pair_id``` - representing the required pair (mandatory)

```python
class KEYS(Enum):
    EXCHANGE = 'exchange_symbol'
    PAIR = 'pair_symbol'

    EXCHANGE_ID = 'exchange_id'
    PAIR_ID = 'pair_id'
```

You can define explicit and implicit symbols to reduce the number of calls 

3. The results of the [CryptowatchPricesPoller](data_pollers/cryptowatch/prices.py) should be saved in the 
db defined in the config file.

The results should be normalized so that every result will contain the structure (as defined by 
[CryptowatchPriceResult](nissy999/mc-test/blob/master/common/structs/cryptowatch/prices.py)):

```json
{
  "_id": ObjectId("63319be3298d4ebc95a0c125"),
  "price": 20154.5,
  "exchange": {
    "_id": ObjectId("63319be3298d4ebc95a0be4b"),
    "id": 123, // external id
    "symbol": "btc"
  },
  "pair": {
    "_id": ObjectId("6331a8ad573819f46fca7433"),
    "id": 456, // external id
    "symbol": "usd"
  },
  "date_added" : ISODate("2022-09-27T16:27:08.830+03:00"),
  "last_update" : ISODate("2022-09-27T16:27:08.830+03:00")
}
```

Normalizing the time to the floor minute should be used as a key for querying

Sample config file (should be put in ```CONF_FILE_FOLDER_NAME``` ("mc-test-files" by default) under the project's root:

```json
{
  "mongodb": {
    "cryptowatch": {
      "name": "mctest",
      "host": "127.0.0.1",
      "port": 27017
    }
  },
  "logging": {
    "level": "debug",
    "handlers": {
      "file": {
        "enabled": true,
        "filepath": "/opt/src/mc-test/mc-test.log"
      },
      "stdout": {
        "enabled": true
      },
      "syslog": {
        "enabled": false
      }
    },
    "formatter": "%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s"
  }
}
```

### Flask API

A simple and small API (single method) which takes into account Quotes (prices) are stored in the DB 
using the data-pollers

The entrypoint is at [rest_api/start_rest_api.py](nissy999/mc-test/blob/master/rest_api/start_rest_api.py)

There is only a single request with the router "/quotes/<string:base_symbol>/<string:quote_symbol>"

When a request is made
* The base and quote assets are loaded from the db
* All the pairs containing the base and quote assets are loaded
* For each pair all the exchanges are loaded
* The result are series of all the prices since a given time (hard coded as last hour) for all the exchanges

It is possible to configure explicit/implicit exchanges


### Rank Calculation

When taking into account all the data is stored in the DB (using the "system" option):

1. Once every 24 hours we should run the rank calculator for each of the pairs we are interested to monitor. 
The rank calculator can include a specific exchange (for better comparison of each daily change). 
or we can run the calculator for each exchange separately (each price record contains the exchange info)
2. We should load all the data from the last 24 hours based on the parameters passed from the scheduler per segment.
3. The data should be loaded to a [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) 
on which we can run the mean function easily on large dataset.
Although I generally prefer not to use MongoDB's aggregation framework it is very handy when it comes to flattening
multi level records/documents, used by columnar packages such as pandas, numpy and scipy.

```javascript
db.CryptoWatchPrices.aggregate([
    {
        $match: {'base.symbol': 'btc'}
    },
    {
        $project: {
            'base_id': '$base._id', 'base_symbol': '$base.symbol', 'base_eid': '$base.external_id',
            'quote_id': '$quote._id', 'quote_symbol': '$quote.symbol', 'quote_eid': '$quote.external_id',
            'price': '$price', 'last_update': '$last_update'
            
        }
    }
])
```

The result is a "flat" dict containing only the relevant fields which can be loaded "as is" to a DAtaFrame object.

4. The result of each mean function should be stored for further processing
5. After all 4. steps are done we can calculate the deviation by comparing to other metrics (GOLD/ETH) and store 
the results back for others to consume.

<sup>* see scheduling in previous sections</sup>

## Scalability

Assumption - the number of API requests is not an issue and the API can answer to as many requests as 
necessary concurrently

1. Increasing the number of running pollers. The number of pollers should be a factor of the number of required operations. 
If we consider we track 3 metrics, cover 4 exchanges, per 30 seconds interval we must make ```3 * 4 * 2 = 24``` 
requests every minute just to track the prices (without maintaining the other aspects - assets/markets/pairs).
The number of concurrent pollers is subject to implementation. You could use a different poller (as a lambda) 
for each combination, initialize it with those parameters and let it "die" upon finish (expensive). You can 
fill a tasks queue (SQS/Kafka) and let each poller work continuously until it gets no data. We should collect 
metrics (api is the external api):
   * api_time: API poll time
   * api_response_processing_time: parsing+enriching+saving to repository 
   * api_response_resources: CPU+memeory 
   * db_load: IO+CPU+Memory(swap)
   * not complete - still need work


2. Based on the metrics collected in 1 we can get a better idea on the number of pollers required for the application

3. Scaling the db
   * Vertically or horizontally (vendor dependent)
   * Separating insert+update+delete calls which should run on against the primary vs "select/find/get" queries
which should be run against a replica-set
   * Sharding - different currencies should be stored in different shard. Can be alphabetically (currencies starting 
the letters A-G on shard A) or by usage (e.g. BTC on shard A, ETH on shard B. Better for performance but more complex to manage) 
   * Smart retention policy to save aggregated data and query it 


