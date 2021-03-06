
import sys
from codecs import getwriter


API_PATH = '/mockernaut'

DATABASE_HOST = '127.0.0.1'

DATABASE_PORT = 3306

DATABASE_USER = 'root'

DATABASE_PASSWORD = ''

DATABASE_NAME = 'mockernaut'

DATABASE_POOL_SIZE = 5

LOGGER_NAME = 'mockernaut'

LOGGING = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': getwriter('utf-8')(sys.stderr),
            'formatter': 'basic'
        },
        'null': {
            'class': 'mockernaut.compat.NullHandler',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        LOGGER_NAME: {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
}
