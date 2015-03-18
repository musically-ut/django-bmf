# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0005_dms_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='sha1',
            field=models.CharField(editable=False, max_length=40, verbose_name='SHA1', null=True),
            preserve_default=True,
        ),
    ]
