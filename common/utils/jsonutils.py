import datetime
import decimal
import uuid
from json import JSONEncoder
from typing import Any, Optional

from bson import ObjectId

from common.consts import LIST_TYPES


def JsonEncoderJS_default(obj: Any) -> Any:
    if isinstance(obj, (str, int, float, bool)):
        pass
    elif isinstance(obj, datetime.datetime):
        obj = obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        obj = float(obj)
    elif isinstance(obj, (ObjectId, uuid.UUID)):
        obj = str(obj)
    elif isinstance(obj, bytes):
        obj = obj.decode('utf-8')
    else:
        obj = obj.__dict__
    return obj


class JsonEncoderJS(JSONEncoder):

    def default(self, obj: Any) -> Any:
        return JsonEncoderJS_default(obj)

    def encode(self, o: Any) -> str:
        o = remove_invalid_keys(o, self=self)
        return super().encode(o)

    @classmethod
    def json_encode(cls, obj: Any) -> str:
        return cls().encode(obj)


def remove_invalid_keys(obj: Any,
                        self: Optional[JSONEncoder]) -> Any:
    if obj is None:
        return obj
    elif isinstance(obj, (str, int, float, bool)):
        return obj
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, (ObjectId, uuid.UUID)):
        return str(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, dict):
        return {
            remove_invalid_keys(k, self=self): remove_invalid_keys(v, self=self)
            for k, v in obj.items()
        }
    elif isinstance(obj, LIST_TYPES):
        return [remove_invalid_keys(_, self=self) for _ in obj]
    elif self:
        return JSONEncoder.default(self, obj)
    else:
        return obj
