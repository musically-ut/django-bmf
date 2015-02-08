# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangobmf_team', '0002_version_0_2_0'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teammember',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teammember',
            name='modified',
            field=models.DateTimeField(null=True, auto_now=True, verbose_name='Modified'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teammember',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teammember',
            name='uuid',
            field=models.CharField(verbose_name='UUID', blank=True, max_length=100, editable=False, db_index=True, null=True),
            preserve_default=True,
        ),
    ]
