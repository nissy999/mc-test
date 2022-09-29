"""
Responsible for managing config settings
"""
import os
from typing import Optional, Union, Dict, Any

from common.utils.collectionsutils import RDict

try:
    # allow remarks in config file
    import jstyleson as json
except ImportError:
    import json

from common.consts import APP_NAME, CONF_FILE_FOLDER_NAME


DEFAULT_CONF_FILE_NAME = 'main.conf'

_conf_files_folder_candidates = (f'../{CONF_FILE_FOLDER_NAME}',
                                 f'/etc/{APP_NAME}',
                                 os.path.abspath(os.path.join(os.path.dirname(__file__), '../',
                                                              CONF_FILE_FOLDER_NAME)),
                                 os.path.abspath(os.path.join(os.path.dirname(__file__), '../..',
                                                              CONF_FILE_FOLDER_NAME)))

_conf_files: RDict = RDict()


def get_abs_file_name(file_name: str,
                      folder_name: Optional[str] = None) -> str:
    return file_name \
        if os.path.isabs(file_name) or not folder_name else \
        os.path.join(folder_name, file_name)


def file_exists(file_name: str,
                folder_name: Optional[str] = None):
    abs_file_name = get_abs_file_name(file_name=file_name, folder_name=folder_name)
    return os.path.isfile(abs_file_name)


def _read_file(filename: str,
               to_json: Optional[bool] = True) -> Optional[Union[str, RDict]]:
    # iterate through the folders and find the first file found
    file_full_path = next((get_abs_file_name(file_name=filename, folder_name=folder_candidate)
                           for folder_candidate in _conf_files_folder_candidates
                           if file_exists(file_name=filename, folder_name=folder_candidate)), None)
    if not file_full_path:
        return None

    content: Union[str, Dict[str, Any]]
    with open(file_full_path, 'r') as fs:
        content = fs.read()

    if to_json:
        content = json.loads(content)
        content = RDict(content)

    return content


_cnf: RDict = _read_file(filename=DEFAULT_CONF_FILE_NAME)


def get(key: str,
        default: Optional[Any] = None) -> Optional[Any]:
    return _cnf.get(key=key, default=default)


cnf_get = get
