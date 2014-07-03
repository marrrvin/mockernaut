
from json import dumps

from flask import Flask
from flask import request
from werkzeug.wrappers import Response
from werkzeug._compat import string_types

from .views.api import rules
from .views.proxy import proxy
from .storage import storage_class
from .compat import text_type
from .compat import dictConfig
from .errors import HTTPException
from .errors import ValidationError
from .errors import DoesNotExists
from .errors import MultipleChoice


class JsonResponse(Response):
    default_mimetype = 'application/json'


class App(Flask):
    response_class = JsonResponse

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.serializable_types = (text_type, bytes, bytearray, list, dict)

    def make_response(self, rv):
        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

        if rv is None:
            raise ValueError('View function did not return a response')

        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        if not isinstance(rv, self.response_class):
            # When we create a response object directly, we let the constructor
            # set the headers and status.  We do this because there can be
            # some extra logic involved when creating these objects with
            # specific values (like default content type selection).
            if isinstance(rv, self.serializable_types):
                rv = dumps(rv)

                rv = self.response_class(rv, headers=headers,
                                         status=status_or_headers)
                headers = status_or_headers = None
            else:
                rv = self.response_class.force_type(rv, request.environ)

        if status_or_headers is not None:
            if isinstance(status_or_headers, string_types):
                rv.status = status_or_headers
            else:
                rv.status_code = status_or_headers
        if headers:
            rv.headers.extend(headers)

        return rv


EXCEPTION_TO_STATUS_CODE = {
    ValidationError: 400,
    DoesNotExists: 404,
    MultipleChoice: 409
}


SUPPORTED_HTTP_CODES = (
    400, 401, 403, 404, 405, 409, 410, 500
)


def handle_exception(exc):
    exc_class = exc.__class__

    if isinstance(exc, HTTPException):
        status_code = exc.code

        error = {
            'type': exc_class.__name__,
            'message': exc.message
        }
    else:
        try:
            status_code = EXCEPTION_TO_STATUS_CODE[exc_class]
        except KeyError:
            status_code = 500

        error = {
            'type': exc_class.__name__,
            'message': text_type(exc)
        }

    return error, status_code


def create_app():
    app = App(__name__)

    app.config.from_envvar('MOCKERNAUT_SETTINGS')

    dictConfig(app.config['LOGGING'])

    app.logger.info(
        'Init storage {user}@{host}:{port}/{name}?pool_size={size}'.format(
            user=app.config['DATABASE_USER'],
            host=app.config['DATABASE_HOST'],
            port=app.config['DATABASE_PORT'],
            name=app.config['DATABASE_NAME'],
            size=app.config['DATABASE_POOL_SIZE']
        ))

    storage = storage_class(
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
        user=app.config['DATABASE_USER'],
        passwd=app.config['DATABASE_PASSWORD'],
        database=app.config['DATABASE_NAME'],
        pool_size=app.config['DATABASE_POOL_SIZE']
    )

    app.logger.info('Clear storage.')
    storage.clear()

    app.storage = storage

    app.logger.debug('Register blueprints.')
    app.register_blueprint(
        proxy, url_prefix='/'
    )
    app.register_blueprint(
        rules, url_prefix='{api_path}'.format(api_path=app.config['API_PATH'])
    )

    app.logger.debug('Register error handler.')
    app.register_error_handler(Exception, handle_exception)

    for code in SUPPORTED_HTTP_CODES:
        app.register_error_handler(code, handle_exception)

    return app
