from typing import Dict, Any, Optional, List, Union, Tuple

import pymongo

from common.enums.bases import Enum
from common.logs.logger import Logger


CONFIG_SECTION_NAME = 'mongodb'
DEFAULT_DB_NAME = 'default_db'


__connections__ = {
    CONFIG_SECTION_NAME: None,
}


class DATABASES(Enum):
    CRYPTOWATCH = 'cryptowatch'


def _parse_db_connections(config: Optional[Dict[str, Any]],
                          update: bool = False,
                          default_db: Optional[str] = None) -> Dict[str, Any]:
    params = {
        db_name: {
            'dbname': settings.get('name') or settings.get('dbname') or db_name,
            'host': settings.get('host') or pymongo.MongoClient.HOST,
            'port': settings.get('port') or pymongo.MongoClient.PORT
            # 'username': settings.get('username'),
            # 'password': settings.get('password')
        }
        for db_name, settings in config.items()
    }

    if update:
        __connections__[CONFIG_SECTION_NAME] = params

    if isinstance(default_db, str) and default_db.strip:
        __connections__[DEFAULT_DB_NAME] = default_db

    return params


def _initialize():
    if __connections__[CONFIG_SECTION_NAME] is None:
        from common.cnf.handler import cnf_get
        config = cnf_get(CONFIG_SECTION_NAME)

        _parse_db_connections(config=config or {},
                              update=True,
                              default_db=DATABASES.CRYPTOWATCH)


def get_client(db_name: Optional[str] = None,
               config: bool = False) -> Union[pymongo.MongoClient, Tuple[pymongo.MongoClient, Dict[str, Any]]]:
    _initialize()

    if not db_name:
        db_name = __connections__[DEFAULT_DB_NAME]

    _config = __connections__[CONFIG_SECTION_NAME].get(db_name)
    if not _config:
        Logger.error_raise(f'invalid db_name (no config): "{str(db_name)}"')

    client: pymongo.MongoClient = pymongo.MongoClient(**{k: v for k, v in _config.items() if k != 'dbname'})
    if config:
        return client, _config
    return client


def get_db(db_name: Optional[str] = None) -> pymongo.database.Database:
    client: pymongo.MongoClient
    config: Dict[str, Any]
    client, config = get_client(db_name, config=True)
    return getattr(client, config.get('dbname') or db_name)


def get_collection(collection_name: str,
                   db_name: Optional[str] = None) -> pymongo.collection.Collection:
    db = get_db(db_name=db_name)
    return getattr(db, collection_name)


def has_db(name: str) -> bool:
    _initialize()
    return True if __connections__.get(name) else False

