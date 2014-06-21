import unittest2

from mockernaut.client.rule import Rule


class RuleTestCase(unittest2.TestCase):
    def test_base(self):
        r = Rule()
        r.request.path = '/'
        r.request.methods = ('GET', 'DELETE')
        r.request.body = 'Test'
        r.response.headers = [('Content-type', 'application/json')]
        r.response.status = 200
        r.response.body = 'OK'

        r_data = r.to_dict()

        self.assertIsInstance(r_data, dict)
