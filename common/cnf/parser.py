import os
from typing import Optional, Dict, Any, List

try:
    import jstyleson as json
except ImportError:
    import json


def _read_config_file(config_file: str) -> Dict[str, Any]:
    if not os.path.isfile(config_file):
        raise ValueError(f'invalid config file: "{config_file}"')

    with open(config_file, 'r') as fs:
        return json.load(fs)


def read_instructions_file(instructions_file: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(instructions_file):
        raise ValueError(f'invalid instructions file: "{instructions_file}"')

    with open(instructions_file, 'r') as fs:
        content: str = fs.read()

    try:
        return json.loads(content)
    except Exception as ex:
        if not content.startswith('{'):
            content = f'{{{content}}}'
            return json.loads(content)


def parse_config_instructions(config_file: str) -> List[Dict[str, Any]]:
    config: Dict[str, Any] = _read_config_file(config_file)

    log_settings = config.get('logging')
    if log_settings:
        from common.logs.logger import Logger
        Logger.initialize(**log_settings)

    db_settings = config.get('db')
    if db_settings:
        from common.dbmodel.connector import parse_db_config
        parse_db_config(config=db_settings, set_default=True)

    instructions = config.get('instructions')
    if instructions:
        if isinstance(instructions, str):
            instructions = read_instructions_file(instructions)

    if instructions:
        return instructions
