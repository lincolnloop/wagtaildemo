import json
import os
from urlparse import urlparse
import dj_database_url

from .base import *

# Read deployment variables from file
_deploy_config_path = os.environ.get('DEPLOY_CONFIG_FILE',
                                    '/srv/wagtaildemo/deploy_env.json')
with open(_deploy_config_path) as _deploy_config_file:
    DEPLOY_CONFIG = json.load(_deploy_config_file)

DEBUG = False

DATABASES = {
    'default': dj_database_url.parse(
        DEPLOY_CONFIG.get('DATABASE_URL'))
}
SECRET_KEY = DEPLOY_CONFIG.get('SECRET_KEY')
ALLOWED_HOSTS = DEPLOY_CONFIG.get('ALLOWED_HOSTS')

# Drop static files outside the source directory,
# but inside the versioned virtualenv
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s [%(process)d] [%(levelname)s] ' +
                'pathname=%(pathname)s lineno=%(lineno)s ' +
                'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
}


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'URLS': ['http://{}:9200'.format(h) for h in DEPLOY_CONFIG.get('ES_HOSTS')],
        'INDEX': 'wagtaildemo'
    }
}

# Parse redis://host:port/db
_cache_urlparsed = urlparse(DEPLOY_CONFIG.get('CACHE_URL'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': _cache_urlparsed.netloc,
        'KEY_PREFIX': 'wagtaildemo',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'DB': _cache_urlparsed.path.strip('/'),
        }
    }
}

# Use the cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

BROKER_URL = DEPLOY_CONFIG.get('BROKER_URL')
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_COLOR = False
