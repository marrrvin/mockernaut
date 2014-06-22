
import sys
import json

if sys.version_info[:2] < (2, 7):  # pragma: no cover
    import unittest2 as unittest
else:
    import unittest


from mockernaut.app import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.app.storage.delete_all()

        self.client = self.app.test_client()


def loads(data):
    return json.loads(data.decode('utf-8'))