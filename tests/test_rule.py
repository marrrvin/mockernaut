
from mockernaut.tests import ApiTestCase

from mockernaut.client.rule import rule


class RuleTestCase(ApiTestCase):
    def test_base(self):
        r = rule({}, {})

        self.assertIsInstance(r, dict)
