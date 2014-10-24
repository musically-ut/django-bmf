# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0005_removed_m2m_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='draft',
            field=models.BooleanField(default=True, editable=False, verbose_name='Draft'),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='account',
            field=models.ForeignKey(null=True, to=settings.BMF_CONTRIB_ACCOUNT, on_delete=django.db.models.deletion.PROTECT, related_name='transactions'),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='transaction',
            field=models.ForeignKey(null=True, to=settings.BMF_CONTRIB_TRANSACTION, related_name='items'),
        ),
    ]
