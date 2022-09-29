import logging
import os
import re
import sys
from typing import Optional, Callable

import flask

from common.utils.httputils import set_login_url

from common.logs.logger import Logger
from common.utils.jsonutils import JsonEncoderJS


def get_base_app(root_folder: Optional[str] = None,
                 name: Optional[str] = None,
                 templates_folder: Optional[str] = None,
                 static_folder: Optional[str] = None,
                 debug_machine: Optional[bool] = False,
                 debug: Optional[bool] = False,
                 jwt_key_setting_name: Optional[str] = None,
                 jwt_callable: Optional[Callable] = None) -> flask.Flask:
    if not root_folder:
        root_folder = os.getcwd()
    if not name:
        name = __name__
    if not templates_folder:
        templates_folder = os.path.join(root_folder, 'templates')
    if not static_folder:
        static_folder = os.path.join(root_folder, 'static')

    app = flask.Flask(name,
                      template_folder=templates_folder,
                      static_folder=static_folder,
                      root_path=root_folder)
    for handler in Logger.handlers:
        app.logger.addHandler(handler)
    if debug:
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.debug = True
        app.config['TESTING'] = True

    app.secret_key = os.urandom(16).hex()
    app.json_encoder = JsonEncoderJS

    return app


__DEFAULT_TOKEN_LOCATION__ = ['headers']


def add_app_blueprints(app):

    from rest_api.blueprints.quotes import blueprint
    app.register_blueprint(blueprint)

    return app


__NAME__ = 'Monte-Carlo-Assignment-API'


set_login_url('/login')
app = get_base_app(root_folder=os.getcwd(), name=__NAME__,)
app = add_app_blueprints(app)


_DEFAULTS = {
    'listening_ip': '0.0.0.0',
    'listening_port': 5000,
    'debug': False
}


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__NAME__)
    parser.add_argument('-s', '--host', type=str, help='Host', default=_DEFAULTS['listening_ip'])
    parser.add_argument('-p', '--port', type=int, help='Port', default=_DEFAULTS['listening_port'])
    parser.add_argument('-d', '--debug', type=bool, help='Debug Mode', default=_DEFAULTS['debug'])

    args = parser.parse_args()

    app.run(host=args.host, port=int(args.port), debug=args.debug)


if __name__ == '__main__':
    main()
