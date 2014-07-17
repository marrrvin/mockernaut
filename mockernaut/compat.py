
import sys
import logging


PY3 = sys.version_info[0] >= 3

if PY3:
    from urllib.parse import urljoin
    from urllib.parse import urlparse

    from unittest import mock

    text_type = str

    iteritems = dict.items
else:
    from urlparse import urljoin
    from urlparse import urlparse

    import mock

    text_type = unicode

    iteritems = dict.iteritems


if sys.version_info[:2] < (2, 7):  # pragma: no cover
    import unittest2 as unittest

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

    from mockernaut.utils.dictconfig import dictConfig
else:
    import unittest

    from logging import NullHandler
    from logging.config import dictConfig
