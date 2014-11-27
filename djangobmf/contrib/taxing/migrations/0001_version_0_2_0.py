# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('djangobmf_taxing', '0001_initial'), ('djangobmf_taxing', '0002_version_0_2_0')]

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_ACCOUNT),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)),
                ('uuid', models.CharField(db_index=True, editable=False, blank=True, null=True, max_length=100, verbose_name='UUID')),
                ('name', models.CharField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=5, max_digits=8)),
                ('passive', models.BooleanField(default=False, verbose_name='Tax is allways included in the product price and never visible to the customer')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('account', models.ForeignKey(related_name='tax_liability', on_delete=django.db.models.deletion.PROTECT, to=settings.BMF_CONTRIB_ACCOUNT)),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False, blank=True, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Tax',
                'ordering': ['name'],
                'swappable': 'BMF_CONTRIB_TAX',
                'abstract': False,
                'verbose_name_plural': 'Taxes',
            },
            bases=(models.Model,),
        ),
    ]
