
from json import dumps

from mockernaut.compat import mock
from mockernaut.tests import TestCase
from mockernaut.client import Client


class ClientTestCase(TestCase):
    def setUp(self):
        self.base_url = 'http://non-existent-url-13fff2s7f38s78.com'
        self.api_path = '/mockernaut/'
        self.client = Client(base_url=self.base_url, api_path=self.api_path)

        self.rule_data = {
            u'id': 1,
            u'request': {
                u'path': u'/',
            },
            u'response': {
                u'status': 200,
                u'headers': [[u'Content-type', u'application/json']],
                u'body': u'OK'
            },
        }

    @mock.patch('mockernaut.client.requests.get')
    def test_get(self, get_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = self.rule_data
        get_mock.return_value = response_mock

        actual_rule = self.client.get(self.rule_data['id'])

        get_mock.assert_called_once_with(
            self.base_url + self.api_path + str(self.rule_data['id'])
        )

        self.assertEquals(actual_rule, self.rule_data)

    @mock.patch('mockernaut.client.requests.get')
    def test_list(self, get_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = [self.rule_data]
        get_mock.return_value = response_mock

        rule_list = self.client.list()

        self.assertIsInstance(rule_list, list)

        actual_rule = rule_list.pop()

        get_mock.assert_called_once_with(self.base_url + self.api_path)

        self.assertEquals(actual_rule, self.rule_data)

    @mock.patch('mockernaut.client.requests.post')
    def test_add(self, post_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = self.rule_data
        post_mock.return_value = response_mock

        actual_rule = self.client.add(self.rule_data)

        post_mock.assert_called_once_with(
            self.base_url + self.api_path,
            data=dumps(self.rule_data)
        )

        self.assertEqual(actual_rule, self.rule_data)

    @mock.patch('mockernaut.client.requests.delete')
    def test_delete(self, delete_mock):
        response_mock = mock.MagicMock()
        response_mock.json.return_value = ''
        delete_mock.return_value = response_mock

        actual_result = self.client.delete(self.rule_data['id'])

        delete_mock.assert_called_once_with(
            self.base_url + self.api_path + str(self.rule_data['id'])
        )

        self.assertEqual(actual_result, '')
