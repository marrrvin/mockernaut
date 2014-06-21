
from urlparse import urljoin
from json import dumps
import urlparse

import requests


class Client(object):
    def __init__(self, base_url):
        self._base_url = base_url

    def get(self, _id):
        response = requests.get(
            urljoin(self._base_url, '/rules/{_id}'.format(_id=_id))
        )

        return response.json()

    def list(self):
        response = requests.get(
            urljoin(self._base_url, '/rules'),
        )

        return response.json()

    def add(self, rule):
        response = requests.post(
            urljoin(self._base_url, '/rules'),
            data=dumps(rule)
        )

        return response.json()

    def delete(self, _id):
        response = requests.post(
            urljoin(self._base_url, '/rules/{_id}'.format(_id=_id))
        )

        return response.json()
