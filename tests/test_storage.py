
import unittest2

from mockernaut.server import create_app


class ApiTestCase(unittest2.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

        self.app.storage.delete_all()


class StorageTestCase(ApiTestCase):
    def test_base(self):
        storage = self.app.storage

        rule_data = {
            u'request': {
                u'path': u'/',
            },
            u'response': {
                u'status': 200,
                u'headers': [[u'Content-type', u'application/json']],
                u'body': u'OK'
            },
        }
        item = storage.add(rule_data)
        _id = item['id']

        actual_item = storage.get_by_id(_id)
        self.assertEquals(item, actual_item)

        self.assertIsNone(storage.delete_by_id(_id))
