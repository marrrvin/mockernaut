
from werkzeug.exceptions import HTTPException
from jsonschema import ValidationError


class DoesNotExists(Exception):
    pass


class MultipleChoice(Exception):
    pass
