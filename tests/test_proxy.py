
from flask.json import loads

from mockernaut.tests import TestCase


class ApiTestCase(TestCase):
    def test_no_rule(self):
        response = self.client.get('/')

        self.assertEqual(404, response.status_code)
        self.assertEqual('application/json', response.content_type)
        error = loads(response.data)

        self.assertIsInstance(error, dict)
        self.assertIn('type', error)
        self.assertEqual(error['type'], 'DoesNotExist')

    def test_match_single_rule(self):
        status_code = 404
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
            },
            u'response': {
                u'status': status_code,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'Not found'
            },
        })

        response = self.client.get('/')

        self.assertEqual(status_code, response.status_code)
        self.assertEqual(content_type, response.content_type)
        self.assertEqual(b'Not found', response.data)

    def test_match_same_path_different_methods(self):
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
                u'methods': ['GET']
            },
            u'response': {
                u'status': 405,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'GET'
            },
        })
        self.storage.create({
            u'request': {
                u'path': u'/',
                u'methods': ['POST']
            },
            u'response': {
                u'status': 200,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'POST'
            },
        })

        response = self.client.post('/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(content_type, response.content_type)
        self.assertEqual(b'POST', response.data)

    def test_match_same_path_vary_on_arg(self):
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
                u'methods': ['GET'],
            },
            u'response': {
                u'status': 200,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'Simple GET'
            },
        })
        args = {
            'key': 'value'
        }
        self.storage.create({
            u'request': {
                u'path': u'/',
                u'methods': ['GET'],
                u'args': args
            },
            u'response': {
                u'status': 200,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'GET and arg'
            },
        })

        response = self.client.get('/' + '?key=value')

        self.assertEqual(200, response.status_code)
        self.assertEqual(content_type, response.content_type)
        self.assertEqual(b'GET and arg', response.data)
