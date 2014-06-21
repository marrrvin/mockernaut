from unittest import TestCase

from mockernaut.client import Client

"""
class ClientTestCase(TestCase):
    def setUp(self):
        self.client = Client(base_url='http://example.com/')

    def test_get(self):
        rule = self.client.get(1)

        self.assertIsInstance(rule, dict)

    def test_list(self):
        rule_list = self.client.list(1)

        self.assertIsInstance(rule_list, list)

    def test_add(self):
        rule = self.client.add({})

        self.assertIsInstance(rule, dict)

    def test_delete(self):
        self.client.delete(1)

        self.assertTrue(True)
"""