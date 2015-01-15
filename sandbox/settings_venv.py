from sandbox.settings_common import *

# OLD BELOW THIS LINE -----------------------------------------------------------------------------

# Common settings for testing

import os
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

# OLD OVER THIS LINE ------------------------------------------------------------------------------

try:
    from settings_local import *
except:
    pass
