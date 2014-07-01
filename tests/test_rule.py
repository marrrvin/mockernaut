
from mockernaut.tests import SimpleTestCase

from mockernaut.client.rule import rule


class RuleTestCase(SimpleTestCase):
    def test_base(self):
        r = rule({}, {})

        self.assertIsInstance(r, dict)
