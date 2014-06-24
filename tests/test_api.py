from json import dumps

from mockernaut.tests import ApiTestCase
from mockernaut.tests import loads


class RulesListTestCase(ApiTestCase):
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
            '{path}/{_id}'.format(path=self.path, _id=0)
        )

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content_type, 'application/json')

        error = loads(response.data)

        self.assertIsInstance(error, dict)


class CreateRuleTestCase(ApiTestCase):
    def test_create_rule_valid_data(self):
        rule_data = {
            'request': {
                'path': '/'
            },
            'response': {
                'status': 200,
                'headers': [['content-type', 'application/json']],
                'body': 'OK'
            },
        }

        response = self.client.post(self.path, data=dumps(rule_data))

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.content_type, 'application/json')

        rule = loads(response.data)

        self.assertIsInstance(rule, dict)

    def test_create_rule_invalid_data(self):
        rule_data = {
            'request': 'error',
            'wrong-field': None
        }

        response = self.client.post(self.path, data=dumps(rule_data))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content_type, 'application/json')

        rule = loads(response.data)

        self.assertIsInstance(rule, dict)


class DeleteRuleTestCase(ApiTestCase):
    def test_delete_existent_rule(self):
        response = self.client.delete(
            '{path}/{_id}'.format(path=self.path, _id=0)
        )

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.data, '')

    def test_delete_non_existent_rule(self):
        response = self.client.delete(
            '{path}/{_id}'.format(path=self.path, _id=0)
        )

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.data, '')
