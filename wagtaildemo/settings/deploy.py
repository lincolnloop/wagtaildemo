import os
from ConfigParser import ConfigParser
import dj_database_url

from .base import *

DEPLOY_CONFIG = ConfigParser()
DEPLOY_CONFIG.read('/etc/wagtail_deploy.ini')

DEBUG = False

DATABASES = {
    'default': dj_database_url.parse(
        DEPLOY_CONFIG.get('default', 'DATABASE_URL'))
}
SECRET_KEY = DEPLOY_CONFIG.get('default', 'SECRET_KEY')
ALLOWED_HOSTS = DEPLOY_CONFIG.get('default', 'ALLOWED_HOSTS').split(',')

STATIC_ROOT = DEPLOY_CONFIG.get('default', 'STATIC_ROOT')

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
        'URLS': DEPLOY_CONFIG.get('default', 'ES_HOSTS').split(','),
        'INDEX': 'wagtaildemo'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': DEPLOY_CONFIG.get('default', 'CACHE_HOST'),
        'KEY_PREFIX': 'wagtaildemo',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
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

BROKER_URL = DEPLOY_CONFIG.get('default', 'BROKER_URL')
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_COLOR = False
