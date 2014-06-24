
from .compat import unittest
from .app import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.app.storage.clear()

        self.client = self.app.test_client()

        self.path = self.app.config['API_PATH']

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
