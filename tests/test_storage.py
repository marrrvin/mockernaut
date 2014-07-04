
from mockernaut.tests import TestCase
from mockernaut.errors import DoesNotExist


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

    def test_crud(self):
        storage = self.app.storage

        rule_list = storage.get_list()
        self.assertEquals(rule_list, [])

        rule = storage.create(self.rule_data)
        _id = rule['id']

        rule_list = storage.get_list()
        actual_rule = rule_list.pop()
        self.assertEquals(rule, actual_rule)

        self.assertEquals(rule_list, [])

        actual_rule = storage.get_by_id(_id)
        self.assertEquals(rule, actual_rule)

        self.assertIsNone(storage.delete_by_id(_id))

        with self.assertRaises(DoesNotExist):
            storage.delete_by_id(_id)
