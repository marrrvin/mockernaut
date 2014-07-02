
import operator

from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app as app

from mockernaut.compat import urlparse


proxy = Blueprint('proxy', __name__)


def find_by_request(req):
    rules = app.storage.get_by_path(req.path)

    score = {}

    for number, rule in enumerate(rules):
        score[number] = 0
        rule_req = rule['request']

        url_parts = urlparse(req.base_url)

        if req.method in rule_req.get('methods', []):
            score[number] += 1

        if url_parts.scheme == rule_req.get('schema'):
            score[number] += 1

        userinfo = '{0}:{1}'.format(url_parts.username, url_parts.password)
        if userinfo == rule_req.get('userinfo'):
            score[number] += 1

        if url_parts.netloc == rule_req.get('host'):
            score[number] += 1

        if url_parts.port == rule_req.get('port'):
            score[number] += 1

        if url_parts.fragment == rule_req.get('port'):
            score[number] += 1

        if req.data == rule_req.get('data'):
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
