
from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app as app

from mockernaut.views.rule import find_rule_by_request


proxy = Blueprint('proxy', __name__)


@proxy.route('', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD'])
def main():
    possible_rules = app.storage.get_list_by_path(request.path)

    rule = find_rule_by_request(possible_rules, request)
    response = rule['response']

    return Response(
        response['body'],
        status=response['status'],
        headers=response['headers']
    )
