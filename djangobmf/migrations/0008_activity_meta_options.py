# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0007_version_0_2_0'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ('-modified',), 'verbose_name': 'Activity', 'get_latest_by': 'modified', 'verbose_name_plural': 'Activity'},
        ),
    ]
