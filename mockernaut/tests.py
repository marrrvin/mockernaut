
from .compat import unittest
from .app import create_app


class SimpleTestCase(unittest.TestCase):
    pass


class TestCase(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

        self.app = create_app()
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

        self.path = self.app.config['API_PATH']

        self.addCleanup(self.app.storage.clear)
