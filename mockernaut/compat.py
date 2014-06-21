
import sys
import operator


PY3 = sys.version_info[0] >= 3

if PY3:
    from urllib.parse import urljoin

    iteritems = operator.methodcaller('items')

    text_type = str
else:
    from urlparse import urljoin

    iteritems = operator.methodcaller('iteritems')

    text_type = unicode
