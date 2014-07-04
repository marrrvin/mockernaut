
import operator

from mockernaut.compat import iteritems
from mockernaut.compat import urlparse
from mockernaut.errors import NoMatch
from mockernaut.errors import MultipleChoice
from mockernaut.errors import DoesNotExist


def match_request(req, rule_req):
    url_parts = urlparse(req.base_url)
    score = 0

    if 'methods' in rule_req:
        if req.method not in rule_req['methods']:
            raise NoMatch
        score += 1

    if 'schema' in rule_req:
        if url_parts.scheme != rule_req['schema']:
            raise NoMatch
        score += 1

    if 'userinfo' in rule_req:
        userinfo = '{0}:{1}'.format(url_parts.username, url_parts.password)
        if userinfo != rule_req['userinfo']:
            raise NoMatch
        score += 1

    if 'host' in rule_req:
        if url_parts.netloc != rule_req['host']:
            raise NoMatch
        score += 1

    if 'port' in rule_req:
        if url_parts.port != rule_req.get('port'):
            raise NoMatch
        score += 1

    if 'fragment' in rule_req:
        if url_parts.fragment != rule_req['fragment']:
            raise NoMatch
        score += 1

    if 'body' in rule_req:
        if req.data != rule_req['body']:
            raise NoMatch
        score += 1

    if 'args' in rule_req:
        for name, value in iteritems(rule_req['args']):
            if value != req.args.get(name):
                raise NoMatch
            score += 1

    if 'form' in rule_req:
        for name, value in iteritems(rule_req['form']):
            if value != req.form.get(name):
                raise NoMatch
            score += 1

    if 'headers' in rule_req:
        for name, value in rule_req['headers']:
            if name in req and req[name] != value:
                raise NoMatch
            score += 1

    return score


def _get_items_with_max_values(dct):
    if not dct:
        return []

    max_value = max(iteritems(dct), key=operator.itemgetter(1))[1]

    return dict([
        (number, value) for number, value in iteritems(dct)
        if value == max_value
    ])


def find_rule_by_request(rules, req):
    scores = {}
    for number, rule in enumerate(rules):
        try:
            scores[number] = match_request(req, rule['request'])
        except NoMatch:
            continue

    if not scores:
        raise NoMatch('No rule.')

    winners = _get_items_with_max_values(scores)
    if len(winners) > 1:
        raise MultipleChoice(
            'More then one rule was found for path={path}.'.format(
                path=req.path
            )
        )

    winner_number, _ = [i for i in iteritems(winners)].pop()

    return rules[winner_number]
