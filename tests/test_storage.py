
import unittest

from mockernaut.server import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()


class StorageTestCase(ApiTestCase):
    def test_base(self):
        storage = self.app.storage

        rule_data = {
            'path': '/',
            'request': {},
            'response': {
                'status': 200,
                'headers': [['Content-type', 'application/json']],
                'body': 'OK'
            },
        }
        item = storage.add(rule_data)

        _id = item.pop('id')

        actual_item = storage.get_by_id(_id)
        self.assertEquals(item, actual_item)

        self.assertTrue(storage.delete_by_id(_id))

        with self.assertRaises(storage.DoesNotExists):
            storage.delete_by_id(_id)
