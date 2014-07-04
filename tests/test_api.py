
from flask.json import loads
from flask.json import dumps

from mockernaut.tests import TestCase


class ApiTestCase(TestCase):
    def setUp(self):
        self.rule_data = {
            u'request': {
                u'path': u'/',
            },
            u'response': {
                u'status': 200,
                u'headers': [[u'Content-type', u'application/json']],
                u'body': u'OK'
            },
        }


class RuleListTestCase(ApiTestCase):
    def test_get_empty_rules_list(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content_type, 'application/json')

        rules_list = loads(response.data)

        self.assertIsInstance(rules_list, list)
        self.assertEquals(len(rules_list), 0)


class GetRuleByIdTestCase(ApiTestCase):
    def test_get_rule_by_non_existent_id(self):
        response = self.client.get(
            '{path}/{id}'.format(path=self.path, id=0)
        )

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content_type, 'application/json')

        error = loads(response.data)

        self.assertIsInstance(error, dict)
        self.assertIn('type', error)
        self.assertEqual(error['type'], 'DoesNotExist')


class CreateRuleTestCase(ApiTestCase):
    def test_create_rule_valid_data(self):
        response = self.client.post(self.path, data=dumps(self.rule_data))

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.content_type, 'application/json')

        rule = loads(response.data)

        self.assertIsInstance(rule, dict)

    def test_create_rule_invalid_data(self):
        rule_data = {
            u'request': 'error',
            u'wrong-field': None
        }

        response = self.client.post(self.path, data=dumps(rule_data))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content_type, 'application/json')

        rule = loads(response.data)

        self.assertIsInstance(rule, dict)


class DeleteRuleTestCase(ApiTestCase):
    def test_delete_existent_rule(self):
        response = self.client.delete(
            '{path}/{id}'.format(path=self.path, id=0)
        )

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.data, b'')

    def test_delete_non_existent_rule(self):
        response = self.client.delete(
            '{path}/{id}'.format(path=self.path, id=0)
        )

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.data, b'')
