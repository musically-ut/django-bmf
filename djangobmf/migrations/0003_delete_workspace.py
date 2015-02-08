# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0002_dashboard_update'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workspace',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='workspace',
            name='ct',
        ),
        migrations.RemoveField(
            model_name='workspace',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Workspace',
        ),
    ]
