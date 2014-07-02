
import os

from flask.json import load

import mockernaut


ROOT_DIR = os.path.dirname(os.path.abspath(mockernaut.__file__))


class DocContainer(object):
    pass


docs = None


def load_schema(name, path):
    global docs

    if not docs:
        docs = DocContainer()

    full_path = os.path.join(ROOT_DIR, path)
    with open(full_path) as fp:
        setattr(docs, name, load(fp))


load_schema('rule', 'schema/rule.json')
