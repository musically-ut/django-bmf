# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0008_activity_meta_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='document',
            name='project',
        ),
        migrations.AddField(
            model_name='document',
            name='customer_pk',
            field=models.PositiveIntegerField(db_index=True, editable=False, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='project_pk',
            field=models.PositiveIntegerField(db_index=True, editable=False, blank=True, null=True),
            preserve_default=True,
        ),
    ]
