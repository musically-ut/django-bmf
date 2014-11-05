#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# keep celery optional
try:
    from celery import shared_task
    CELERY = True
except ImportError:
    CELERY = False

from djangobmf.notification.tasks import djangobmf_user_watch as _djangobmf_user_watch

if CELERY:
    @shared_task
    def djangobmf_celery_user_watch(*args, **kwargs):
        return _djangobmf_user_watch(*args, **kwargs)

def djangobmf_user_watch(*args, **kwargs):
    if CELERY:
        return djangobmf_celery_user_watch.apply_async(args, kwargs)
    return _djangobmf_user_watch(*args, **kwargs)
