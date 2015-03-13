import os
from ConfigParser import ConfigParser
import dj_database_url

from .base import *

DEPLOY_CONFIG = ConfigParser()
DEPLOY_CONFIG.read('/etc/wagtail_deploy.ini')

DEBUG = False

DATABASES = {
    'default': dj_database_url.parse(
        DEPLOY_CONFIG.get('default', 'database_url'))
}


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': 'wagtaildemo'
    }
}


INSTALLED_APPS+= (
    'djcelery',
    'kombu.transport.django'
)


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
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

# CELERY SETTINGS
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://'
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_COLOR = False
