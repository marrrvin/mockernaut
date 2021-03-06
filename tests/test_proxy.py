
from flask.json import loads

from mockernaut.tests import TestCase


class ApiTestCase(TestCase):
    def test_no_rule(self):
        response = self.client.get('/')

        self.assertResponse(response, 404)

        error = loads(response.data)
        self.assertError(error, 'DoesNotExist')

    def test_no_match(self):
        status_code = 200
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
                u'methods': ['POST']
            },
            u'response': {
                u'status': status_code,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'GET 1'
            },
        })

        response = self.client.get('/?key=value')

        self.assertResponse(response, 404)

        error = loads(response.data)
        self.assertError(error, 'NoMatch')

    def test_multiple_choice(self):
        status_code = 200
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
                u'methods': ['GET']
            },
            u'response': {
                u'status': status_code,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'GET 1'
            },
        })
        self.storage.create({
            u'request': {
                u'path': u'/',
                u'args': {'key': 'value'}
            },
            u'response': {
                u'status': status_code,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'GET 1'
            },
        })

        response = self.client.get('/?key=value')

        self.assertResponse(response, 409)

        error = loads(response.data)
        self.assertError(error, 'MultipleChoice')

    def test_match_single_rule(self):
        status_code = 200
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
            },
            u'response': {
                u'status': status_code,
                u'headers': [[u'Content-type', content_type]],
                u'body': u'Single rule'
            },
        })

        response = self.client.get('/')

        self.assertResponse(response, content_type=content_type)
        self.assertEqual(b'Single rule', response.data)

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

        self.assertResponse(response, 200, content_type)
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

        self.assertResponse(response, content_type=content_type)
        self.assertEqual(b'GET and arg', response.data)
