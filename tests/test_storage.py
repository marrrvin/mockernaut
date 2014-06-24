
from mockernaut.tests import ApiTestCase


class StorageTestCase(ApiTestCase):
    def test_base(self):
        storage = self.app.storage

        rule = storage.create(self.rule_data)
        _id = rule['id']

        actual_rule = storage.get_by_id(_id)
        self.assertEquals(rule, actual_rule)

        self.assertIsNone(storage.delete_by_id(_id))
