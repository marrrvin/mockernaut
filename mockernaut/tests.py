
import json

from .compat import unittest


from mockernaut.app import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.app.storage.delete_all()

        self.client = self.app.test_client()

        self.path = self.app.config['API_PATH']


def loads(data):
    return json.loads(data.decode('utf-8'))
