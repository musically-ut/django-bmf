# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('djangobmf', '0004_added_active_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='has_object',
            field=models.BooleanField(verbose_name='Has object', editable=False, default=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='is_active',
            field=models.BooleanField(verbose_name='Is active', editable=False, default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='key',
            field=models.CharField(verbose_name='Key', editable=False, max_length=50, default='default', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='renderer_ct',
            field=models.ForeignKey(null=True, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='renderer_id',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='options',
            field=models.TextField(verbose_name='Options', blank=True, help_text='Options for the renderer. Gets synced with the renderers options'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('key', 'contenttype', 'has_object')]),
        ),
    ]
