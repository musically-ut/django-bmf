from sandbox.settings_common import *

import sys
import tempfile

BMF_DOCUMENT_ROOT = tempfile.mkdtemp(prefix='djangobmf_')
BMF_DOCUMENT_URL = '/documents/'

INSTALLED_APPS += TEST_PROJECT_APPS

BMF_USE_CELERY = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/database.sqlite' % PROJECT_PATH,
    }
}

HAYSTACK_CONNECTIONS = {
     'default': {
         'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
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
    from settings_local import *
except:
    pass
