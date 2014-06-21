
import sys
import operator


PY3 = sys.version_info[0] >= 3

if PY3:
    from urllib.parse import urljoin

    iteritems = operator.methodcaller('items')
else:
    from urlparse import urljoin

    iteritems = operator.methodcaller('iteritems')
