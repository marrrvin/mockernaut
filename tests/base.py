
import unittest

from mockernaut.server import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()
