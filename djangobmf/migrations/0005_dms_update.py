# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        ('djangobmf', '0004_added_active_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='customer_pk',
        ),
        migrations.RemoveField(
            model_name='document',
            name='project_pk',
        ),
        migrations.AddField(
            model_name='document',
            name='customer',
            field=models.ForeignKey(related_name='documents', to=settings.BMF_CONTRIB_CUSTOMER, null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='mimetype',
            field=models.CharField(verbose_name='Mimetype', editable=False, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(related_name='documents', to=settings.BMF_CONTRIB_PROJECT, null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
    ]
