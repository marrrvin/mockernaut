
from mockernaut.tests import TestCase


class ApiTestCase(TestCase):
    def test_one_rule(self):
        status_code = 404
        body = b'Not found'
        content_type = u'text/plain'

        self.storage.create({
            u'request': {
                u'path': u'/',
            },
            u'response': {
                u'status': status_code,
                u'headers': [[u'Content-type', content_type]],
                u'body': body
            },
        })

        resp = self.client.get('/')

        self.assertEqual(status_code, resp.status_code)
        self.assertEqual(content_type, resp.content_type)
        self.assertEqual(body, resp.data)
