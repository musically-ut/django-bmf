#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType

from djangobmf import models as bmfmodels
from djangobmf.sites import site
from djangobmf.models import NumberCycle


# TODO: Check if this is still needed or can be achieved otherwise
def install(sender, created_models, **kwargs):
    for model in [m for m in site.models if hasattr(m, '_bmfmeta') and m._bmfmeta.number_cycle]:
        ct = ContentType.objects.get_for_model(model)
        count = NumberCycle.objects.filter(ct=ct).count()
        if not count:
            obj = NumberCycle(ct=ct, name_template=model._bmfmeta.number_cycle)
            obj.save()

post_migrate.connect(install, sender=bmfmodels, dispatch_uid="install_djangobmf_modules")
