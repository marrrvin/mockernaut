import os
from json import load

import mockernaut


ROOT_DIR = os.path.dirname(os.path.abspath(mockernaut.__file__))


def load_schema(path):
    full_path = os.path.join(ROOT_DIR, path)

    with open(full_path) as fp:
        return load(fp)


RULE = load_schema('schema/rule.json')
