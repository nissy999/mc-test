from typing import Any

from bson.objectid import ObjectId

from common.consts import BOOL_VALUES


__imports__ = {
    'validators': None,
}


def is_bool(candidate: Any) -> bool:
    return candidate is True or candidate is False


def is_int(candidate: Any) -> bool:
    return isinstance(candidate, int) and not is_bool(candidate)


def is_float(candidate: Any) -> bool:
    return isinstance(candidate, (float, int)) and not is_bool(candidate)


_ObjectIdTypes = (ObjectId, str)


def to_ObjectId(candidate: Any,
                skip_type_validation: bool = False) -> ObjectId:
    if skip_type_validation is not True and not isinstance(candidate, _ObjectIdTypes):
        raise TypeError(f'invalid candidate type: "{type(candidate)}"')
    if isinstance(candidate, str):
        candidate = ObjectId(candidate)
    return candidate


def is_ObjectId(candidate: Any) -> bool:
    if not isinstance(candidate, _ObjectIdTypes):
        return False
    try:
        o = to_ObjectId(candidate, skip_type_validation=True)
        return True
    except:
        return False
