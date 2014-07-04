
from werkzeug.exceptions import HTTPException
from jsonschema import ValidationError


class DoesNotExist(Exception):
    pass


class MultipleChoice(Exception):
    pass


class NoMatch(Exception):
    pass
