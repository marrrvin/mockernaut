
from json import dumps

from mockernaut.compat import mock
from mockernaut.tests import ApiTestCase
from mockernaut.client import Client


class ClientTestCase(ApiTestCase):
    def setUp(self):
        self.base_url = 'http://non-existent-url-13fff2s7f38s78.com'
        self.api_path = '/mockernaut/'
        self.client = Client(base_url=self.base_url, api_path=self.api_path)

        self.rule = {
            'id': 1,
            'request': {
                'path': '/'
            },
            'response': {
                'status': 200,
                'headers': [['Content-type', 'application/json']],
                'body': 'OK'
            }
        }

    @mock.patch('mockernaut.client.requests.get')
    def test_get(self, get_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = self.rule
        get_mock.return_value = response_mock

        actual_rule = self.client.get(self.rule['id'])

        get_mock.assert_called_once_with(
            self.base_url + self.api_path + str(self.rule['id'])
        )

        self.assertEquals(actual_rule, self.rule)

    @mock.patch('mockernaut.client.requests.get')
    def test_list(self, get_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = [self.rule]
        get_mock.return_value = response_mock

        rule_list = self.client.list()

        self.assertIsInstance(rule_list, list)

        actual_rule = rule_list.pop()

        get_mock.assert_called_once_with(self.base_url + self.api_path)

        self.assertEquals(actual_rule, self.rule)

    @mock.patch('mockernaut.client.requests.post')
    def test_add(self, post_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = self.rule
        post_mock.return_value = response_mock

        actual_rule = self.client.add(self.rule)

        post_mock.assert_called_once_with(
            self.base_url + self.api_path,
            data=dumps(self.rule)
        )

        self.assertEqual(actual_rule, self.rule)

    @mock.patch('mockernaut.client.requests.delete')
    def test_delete(self, delete_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = ''
        delete_mock.return_value = response_mock

        actual_result = self.client.delete(self.rule['id'])

        delete_mock.assert_called_once_with(
            self.base_url + self.api_path + str(self.rule['id'])
        )

        self.assertEqual(actual_result, '')
