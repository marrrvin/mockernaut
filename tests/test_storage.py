
from mockernaut.base import ApiTestCase


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
