#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.settings import USE_CELERY

from djangobmf.notification.tasks import djangobmf_user_watch as _djangobmf_user_watch


if USE_CELERY:
    from celery import shared_task

    @shared_task
    def djangobmf_celery_user_watch(*args, **kwargs):
        return _djangobmf_user_watch(*args, **kwargs)


def djangobmf_user_watch(*args, **kwargs):
    if USE_CELERY:
        return djangobmf_celery_user_watch.apply_async(args, kwargs)
    return _djangobmf_user_watch(*args, **kwargs)
