# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import djangobmf.fields


class Migration(migrations.Migration):

    replaces = [
        ('djangobmf_task', '0001_initial'),
        ('djangobmf_task', '0003_optional_project'),
        ('djangobmf_task', '0004_added_acl'),
        ('djangobmf_task', '0005_task_in_charge'),
        ('djangobmf_task', '0006_timetracking_by_timesheets'),
        ('djangobmf_task', '0007_version_0_2_0'),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.BMF_CONTRIB_EMPLOYEE),
        migrations.swappable_dependency(settings.BMF_CONTRIB_TEAM),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('uuid', models.CharField(blank=True, editable=False, verbose_name='UUID', db_index=True, null=True, max_length=100)),
                ('state', djangobmf.fields.WorkflowField(editable=False, db_index=True, null=True, blank=True, max_length=32)),
                ('summary', models.CharField(verbose_name='Title', null=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description')),
                ('completed', models.BooleanField(default=False, editable=False, verbose_name='Completed')),
                ('created_by', models.ForeignKey(blank=True, editable=False, related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('employees', models.ManyToManyField(related_name='employees', blank=True, to=settings.BMF_CONTRIB_EMPLOYEE)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('project', models.ForeignKey(blank=True, to=settings.BMF_CONTRIB_PROJECT, null=True)),
                ('referee', models.ForeignKey(related_name='+', blank=True, to=settings.BMF_CONTRIB_EMPLOYEE, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('team', models.ForeignKey(blank=True, to=settings.BMF_CONTRIB_TEAM, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name_plural': 'Goals',
                'verbose_name': 'Goal',
                'permissions': (('can_manage', 'Can manage all goals'),),
                'ordering': ['project__name', 'summary'],
                'abstract': False,
                'swappable': 'BMF_CONTRIB_GOAL',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('uuid', models.CharField(blank=True, editable=False, verbose_name='UUID', db_index=True, null=True, max_length=100)),
                ('state', djangobmf.fields.WorkflowField(editable=False, db_index=True, null=True, blank=True, max_length=32)),
                ('summary', models.CharField(verbose_name='Title', null=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description')),
                ('due_date', models.DateField(null=True, blank=True, verbose_name='Due date')),
                ('completed', models.BooleanField(default=False, editable=False, verbose_name='Completed')),
                ('created_by', models.ForeignKey(blank=True, editable=False, related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('employee', models.ForeignKey(blank=True, to=settings.BMF_CONTRIB_EMPLOYEE, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('goal', models.ForeignKey(blank=True, to=settings.BMF_CONTRIB_GOAL, null=True)),
                ('in_charge', models.ForeignKey(blank=True, editable=False, related_name='+', to=settings.BMF_CONTRIB_EMPLOYEE, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('project', models.ForeignKey(blank=True, to=settings.BMF_CONTRIB_PROJECT, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tasks',
                'verbose_name': 'Task',
                'ordering': ['due_date', 'summary'],
                'abstract': False,
                'swappable': 'BMF_CONTRIB_TASK',
            },
            bases=(models.Model,),
        ),
    ]
