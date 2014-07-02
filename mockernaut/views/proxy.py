
import operator
from collections import defaultdict

from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app as app

proxy = Blueprint('proxy', __name__)


def find_by_request(req):
    score = {}
    rules = app.storage.get_by_path(req.path)

    for number, rule in enumerate(rules):
        score[number] = 0
        rule_req = rule['request']
        if request.method in rule_req.get('methods', []):
            score[number] += 1

    winner_number, best_score = max(
        score.iteritems(), key=operator.itemgetter(1)
    )

    return rules[winner_number]


@proxy.route('', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD'])
def main():
    rule = find_by_request(request)
    response = rule['response']

    return Response(
        response['body'],
        status=response['status'],
        headers=response['headers']
    )
