
from .compat import unittest
from .app import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.app.storage.clear()

        self.client = self.app.test_client()

        self.path = self.app.config['API_PATH']
