from json import dumps

from flask import Flask
from werkzeug.wrappers import Response
from werkzeug._compat import string_types

from .errors import EXCEPTIONS_TO_STATUS_CODES
from .views.api import rules
from .views.proxy import proxy
from .storage import storage_class


class JsonResponse(Response):
    default_mimetype = 'application/json'


class App(Flask):
    response_class = JsonResponse

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    def make_response(self, rv):
        status = headers = None
        if isinstance(rv, tuple):
            rv, status, headers = rv + (None,) * (3 - len(rv))

        if rv is None:
            raise ValueError('View function did not return a response')

        if not isinstance(rv, self.response_class):
            rv = self.response_class(dumps(rv), headers=headers, status=status)
            headers = status = None

        if status is not None:
            if isinstance(status, string_types):
                rv.status = status
            else:
                rv.status_code = status
        if headers:
            rv.headers.extend(headers)

        return rv


def handle_exception(exc):
    exc_class = exc.__class__

    status_code = 500
    for exc_class, code in EXCEPTIONS_TO_STATUS_CODES.iteritems():
        if isinstance(exc, exc_class):
            status_code = code
            break

    error = {
        'type': exc_class.__name__,
        'message': unicode(exc)
    }

    return error, status_code


def create_app():
    app = App(__name__)
    app.config.from_envvar('MOCKERNAUT_SETTINGS')

    app.storage = storage_class(
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
        user=app.config['DATABASE_USER'],
        passwd=app.config['DATABASE_PASSWORD'],
        database=app.config['DATABASE_NAME'],
        pool_size=app.config['DATABASE_POOL_SIZE']
    )

    app.register_blueprint(proxy, url_prefix='/')
    app.register_blueprint(rules, url_prefix='/rules')

    app.register_error_handler(Exception, handle_exception)

    return app
