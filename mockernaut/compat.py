
import sys
import operator
import logging


PY3 = sys.version_info[0] >= 3

if PY3:
    from urllib.parse import urljoin

    import unittest.mock

    iteritems = operator.methodcaller('items')

    text_type = str
else:
    from urlparse import urljoin

    import mock

    iteritems = operator.methodcaller('iteritems')

    text_type = unicode


if sys.version_info[:2] < (2, 7):  # pragma: no cover
    import unittest2 as unittest

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

    from .utils.dictconfig import dictConfig
else:
    import unittest

    from logging import NullHandler
    from logging.config import dictConfig
