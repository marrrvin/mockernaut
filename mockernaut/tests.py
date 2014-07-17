
from mockernaut.compat import unittest
from mockernaut.app import create_app


class SimpleTestCase(unittest.TestCase):
    pass


class TestCase(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

        self.app = create_app()
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()
        self.storage = self.app.storage

        self.path = self.app.config['API_PATH']

        self.addCleanup(self.storage.clear)

    def assertResponse(self,
                       response,
                       status_code=200,
                       content_type='application/json'):
        self.assertEqual(status_code, response.status_code)
        self.assertEqual(content_type, response.content_type)

    def assertError(self, error, error_type):
        self.assertIsInstance(error, dict)
        self.assertIn('type', error)
        self.assertEqual(error['type'], error_type)
