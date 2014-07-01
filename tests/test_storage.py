
from mockernaut.tests import TestCase


class StorageTestCase(TestCase):
    def setUp(self):
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

    def test_base(self):
        storage = self.app.storage

        rule = storage.create(self.rule_data)
        _id = rule['id']

        actual_rule = storage.get_by_id(_id)
        self.assertEquals(rule, actual_rule)

        self.assertIsNone(storage.delete_by_id(_id))
