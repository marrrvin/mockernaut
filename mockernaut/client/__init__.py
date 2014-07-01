
from flask.json import dumps

import requests

from ..compat import urljoin


def join(*parts):
    base = ''

    return ''.join(map(lambda e: urljoin(base, e), parts))


class Client(object):
    def __init__(self, base_url, api_path):
        self._base_url = base_url
        self._api_path = api_path

    def get(self, _id):
        response = requests.get(
            join(self._base_url, self._api_path, '{_id}'.format(_id=_id))
        )

        return response.json()

    def list(self):
        response = requests.get(
            urljoin(self._base_url, self._api_path),
        )

        return response.json()

    def create(self, rule):
        response = requests.post(
            join(self._base_url, self._api_path),
            data=dumps(rule)
        )

        return response.json()

    def delete(self, _id):
        response = requests.delete(
            join(self._base_url, self._api_path, '{_id}'.format(_id=_id))
        )

        return response.json()
