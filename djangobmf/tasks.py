#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.decorators import optional_celery
from djangobmf.notification.tasks import djangobmf_user_watch

import hashlib


__all__ = [
    'djangobmf_user_watch',
    'generate_sha1',
]


@optional_celery
def generate_sha1(pk):
    from djangobmf.models import Document

    obj = Document.objects.get(pk=pk)

    hash = hashlib.sha1()

    f = obj.file.open('rb')
    if f.multiple_chunks():
        for chunk in f.chunks():
            hash.update(chunk)
    else:
        hash.update(f.read())
    f.close()

    Document.objects.filter(pk=pk).update(sha1=hash.hexdigest())
