# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [
        ('djangobmf_employee','0001_initial'),
        ('djangobmf_employee','0002_optional_employee_contact'),
        ('djangobmf_employee','0003_optional_employee_product'),
        ('djangobmf_employee','0004_version_0_2_0'),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PRODUCT),
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, verbose_name='UUID', db_index=True, blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', null=True)),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='Email', null=True)),
                ('phone_office', models.CharField(blank=True, max_length=255, verbose_name='Phone office', null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=255, verbose_name='Phone mobile', null=True)),
                ('fax', models.CharField(blank=True, max_length=255, verbose_name='Fax', null=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.BMF_CONTRIB_CUSTOMER, verbose_name='Contact', blank=True, related_name='bmf_employee', null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, editable=False, blank=True, to=settings.AUTH_USER_MODEL, related_name='+', null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, editable=False, blank=True, to=settings.AUTH_USER_MODEL, related_name='+', null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.BMF_CONTRIB_PRODUCT, verbose_name='Product', blank=True, related_name='bmf_employee', null=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.BMF_CONTRIB_EMPLOYEE, verbose_name='Supervisor', blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, blank=True, related_name='bmf_employee', null=True)),
            ],
            options={
                'verbose_name_plural': 'Employees',
                'abstract': False,
                'verbose_name': 'Employee',
                'ordering': ['name'],
                'swappable': 'BMF_CONTRIB_EMPLOYEE',
            },
            bases=(models.Model,),
        ),
    ]
