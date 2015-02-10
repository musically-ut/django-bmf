from sandbox.settings_common import *

# Django settings

import os
import sys

INSTALLED_APPS += (
    'celery',
)
INSTALLED_APPS += TEST_PROJECT_APPS

# BMF ==============================================================================

BMF_DOCUMENT_ROOT = os.path.join(PROJECT_PATH, "bmf_documents")
BMF_DOCUMENT_URL = '/bmf_documents/'

# LOCAL SETTINGS ==================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'djangobmf',
    },
}

if 'runserver' in sys.argv:

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': None,
    }

try:
    from sandbox.settings_local import *
except:
    pass
