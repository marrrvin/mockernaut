
from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app as app

proxy = Blueprint('proxy', __name__)


def find_by_request(request):
    rules = app.storage.get_by_path(request.path)

    return rules[0]


@proxy.route('')
def main():
    rule = find_by_request(request)
    response = rule['response']

    return Response(
        response['body'],
        status=response['status'],
        headers=response['headers']
    )
