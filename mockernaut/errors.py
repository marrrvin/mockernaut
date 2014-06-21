
from jsonschema import ValidationError


class DoesNotExists(Exception):
    pass


EXCEPTIONS_TO_STATUS_CODES = {
    ValidationError: 400,
    DoesNotExists: 404
}
