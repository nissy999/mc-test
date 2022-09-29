import uuid
from typing import Tuple, Type

UNDEFINED: str = ''.join([str(uuid.uuid4()) for _ in range(2)])

BOOL_VALUES: Tuple[bool, ...] = (True, False)

APP_NAME = 'mc-test'

CONF_FILE_FOLDER_NAME = 'mc-test-files'

LIST_TYPES: Tuple[Type, ...] = (list, tuple, set)

MONGODB_ID = '_id'
