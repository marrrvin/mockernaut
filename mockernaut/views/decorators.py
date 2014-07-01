
from functools import wraps

from flask import request
from flask import g
from flask.json import loads
from jsonschema import validate

from ..compat import text_type


def schema(schema_doc):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            doc = loads(text_type(request.data))
            validate(doc, schema_doc)
            g.doc = doc

            return func(*args, **kwargs)

        return decorated_function

    return decorator
