#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.conf import settings
from django.utils.text import slugify
from django.utils import translation
from django.utils import six

from .. import models as erpcore
from ..numbering.models import NumberCycle


def install(sender, created_models, **kwargs):
    for model in get_models(): # TODO change to django.apps
        if getattr(model, 'ERPMeta', False):

            kwargs = {
                'app_label': model._meta.app_label,
                'model': model._meta.model_name,
            }

            # LOOK: maybe we could move this to a signal
            try:
                ct = ContentType.objects.get(**kwargs)
            except ContentType.DoesNotExist:
                ct = ContentType(**kwargs)
                ct.name = model._meta.verbose_name_raw
                ct.save()

            if model._erpmeta.number_cycle:
                count = NumberCycle.objects.filter(ct=ct).count()
                if not count:
                    obj = NumberCycle(ct=ct, name_template=model._erpmeta.number_cycle)
                    obj.save()
    return None

post_syncdb.connect(install, sender=erpcore, dispatch_uid="install_djangoerp_modules")
