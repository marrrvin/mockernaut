
import responses
from flask.json import dumps

from mockernaut.tests import TestCase
from mockernaut.client import Client
from mockernaut.client import join
from mockernaut.client import HTTPError


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

    @responses.activate
    def test_get(self):
        responses.add(
            responses.GET,
            join(self.base_url, self.api_path, self.rule_data['id']),
            body=dumps(self.rule_data),
            status=200,
            content_type='application/json'
        )

        actual_rule = self.client.get(self.rule_data['id'])
        self.assertEquals(actual_rule, self.rule_data)

    @responses.activate
    def test_list(self):
        responses.add(
            responses.GET,
            join(self.base_url, self.api_path),
            body=dumps([self.rule_data]),
            status=200,
            content_type='application/json'
        )

        rule_list = self.client.list()

        self.assertIsInstance(rule_list, list)

        actual_rule = rule_list.pop()
        self.assertEquals(actual_rule, self.rule_data)

    @responses.activate
    def test_create(self):
        responses.add(
            responses.POST,
            join(self.base_url, self.api_path),
            body=dumps(self.rule_data),
            status=200,
            content_type='application/json'
        )

        actual_rule = self.client.create(self.rule_data)
        self.assertEqual(actual_rule, self.rule_data)

    @responses.activate
    def test_create_bad_request(self):
        responses.add(
            responses.POST,
            join(self.base_url, self.api_path),
            body=dumps({
                u'error': u'ValidationError',
                u'message': u'Invalid field non-existent.'
            }),
            status=400,
            content_type='application/json'
        )

        with self.assertRaises(HTTPError):
            self.client.create(self.rule_data)

    @responses.activate
    def test_delete(self):
        responses.add(
            responses.DELETE,
            join(self.base_url, self.api_path, self.rule_data['id']),
            body=dumps(''),
            status=200,
            content_type='application/json'
        )

        actual_result = self.client.delete(self.rule_data['id'])
        self.assertEqual(actual_result, '')

    @responses.activate
    def test_delete_not_found(self):
        responses.add(
            responses.DELETE,
            join(self.base_url, self.api_path, 0),
            body=dumps({
                u'error': u'NotFound',
                u'message': u'Rule not found.'
            }),
            status=404,
            content_type='application/json'
        )

        with self.assertRaises(HTTPError):
            self.client.delete(0)
