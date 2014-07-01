
from mockernaut.tests import TestCase


class ApiTestCase(TestCase):
    def test_one_rule(self):
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
