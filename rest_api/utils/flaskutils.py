from typing import Optional

import flask


def get_remote_addr(request=None) -> str:
    if not request:
        request = flask.request

    return request.headers.getlist('X-Forwarded-For')[0] if request.headers.getlist("X-Forwarded-For") \
        else request.remote_addr


def flask_abort(msg: str,
                code: int):
    return flask.abort(code, msg)


def raise_bad_request(msg: Optional[str] = None,
                      code: Optional[int] = None,
                      *args, **kwargs):
    return flask_abort(msg=msg if msg else '',
                       code=code if code else 400)


def raise_internal_error(msg: Optional[str] = None,
                         code: Optional[int] = None,
                         *args, **kwargs):
    return flask_abort(msg=msg if msg else '',
                       code=code if code else 500)
