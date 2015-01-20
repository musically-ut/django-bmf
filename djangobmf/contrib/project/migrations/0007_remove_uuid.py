# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_project', '0006_version_0_2_0'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects', 'ordering': ['name'], 'permissions': (('can_manage', 'Can manage all projects'),)},
        ),
        migrations.RemoveField(
            model_name='project',
            name='uuid',
        ),
    ]
