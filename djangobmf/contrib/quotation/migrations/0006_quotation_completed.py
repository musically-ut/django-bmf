# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_quotation', '0005_version_0_2_0'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='Completed', editable=False),
            preserve_default=True,
        ),
    ]
