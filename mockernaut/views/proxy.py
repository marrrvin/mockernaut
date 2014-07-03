
import operator

from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app as app

from mockernaut.compat import iteritems
from mockernaut.compat import urlparse
from mockernaut.errors import DoesNotExists
from mockernaut.errors import MultipleChoice


proxy = Blueprint('proxy', __name__)


def find_rule_by_request(req):
    rules = app.storage.get_by_path(req.path)

    scores = {}
    for number, rule in enumerate(rules):
        rule_req = rule['request']
        url_parts = urlparse(req.base_url)
        score = 0

        if 'methods' in rule_req:
            if req.method not in rule_req['methods']:
                continue
            else:
                score += 1

        if 'schema' in rule_req:
            if url_parts.scheme != rule_req['schema']:
                continue
            else:
                score += 1

        if 'userinfo' in rule_req:
            userinfo = '{0}:{1}'.format(url_parts.username, url_parts.password)
            if userinfo != rule_req['userinfo']:
                continue
            else:
                score += 1

        if 'host' in rule_req:
            if url_parts.netloc != rule_req['host']:
                continue
            else:
                score += 1

        if 'port' in rule_req:
            if url_parts.port != rule_req.get('port'):
                continue
            else:
                score += 1

        if 'fragment' in rule_req:
            if url_parts.fragment != rule_req['fragment']:
                continue
            else:
                score += 1

        if 'body' in rule_req:
            if req.data != rule_req['body']:
                continue
            else:
                score += 1

        if 'args' in rule_req:
            for name, value in iteritems(rule_req['args']):
                if value != req.args.get(name):
                    continue
            score += 1

        if 'form' in rule_req:
            for name, value in iteritems(rule_req['form']):
                if value != req.form.get(name):
                    continue
            score += 1

        if 'headers' in rule_req:
            for name, value in rule_req['headers']:
                if name in req and req[name] != value:
                    continue
            score += 1

        scores[number] = score

    if not scores:
        raise DoesNotExists('Rule not found.')

    max_score = max(iteritems(scores), key=operator.itemgetter(1))[1]
    winner_numbers = {number: score for number, score in iteritems(scores) if score == max_score}

    if len(winner_numbers) > 1:
        raise MultipleChoice('More then one rule found.')

    winner_number, _ = [i for i in iteritems(winner_numbers)][0]

    return rules[winner_number]


@proxy.route('', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD'])
def main():
    rule = find_rule_by_request(request)
    response = rule['response']

    return Response(
        response['body'],
        status=response['status'],
        headers=response['headers']
    )
