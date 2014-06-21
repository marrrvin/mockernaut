from flask import Blueprint
from flask import g
from flask import current_app as app

from .decorators import schema
from .schema import RULE


rules = Blueprint('rules', __name__)


@rules.route('')
def get_rules_list():
    return app.storage.all()


@rules.route('/<int:rule_id>')
def get_rule(rule_id):
    return app.storage.get_by_id(rule_id)


@rules.route('', methods=['POST'])
@schema(RULE)
def add_rule():
    return app.storage.add(g.doc), 201


@rules.route('/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    try:
        app.storage.delete_by_id(rule_id)
    except app.storage.DoesNotExists:
        pass

    return '', 204
