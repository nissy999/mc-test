import os
from typing import Dict, Any

from common.consts import CONF_FILE_FOLDER_NAME

_conf_paths = (f'../{CONF_FILE_FOLDER_NAME}',
               f'/etc/{APP_NAME}',
               os.path.abspath(os.path.join(os.path.dirname(__file__), '../', __FOLDER_NAME__)),
               os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', __FOLDER_NAME__)))


def _load():
    cnf: Dict[str, Any] = {k: v for k, v in os.environ.items()}



    for k, v in iter(os.environ.items()):
        cnf[k] = v
    env_dir = os.getenv('SDCC_HOME', os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    env_file = os.path.join(env_dir, '.env')
    if os.path.isfile(env_file):
        for k, v in dotenv_values(env_file).items():
            cnf[k] = v
    return cnf


_cnf = _load()