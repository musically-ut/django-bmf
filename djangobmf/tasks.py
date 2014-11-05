#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from celery import shared_task

from djangobmf.notification.tasks import djangobmf_user_watch as _djangobmf_user_watch


@shared_task
def djangobmf_user_watch(*args, **kwargs):
    return _djangobmf_user_watch(*args, **kwargs)
