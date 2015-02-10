# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.contrib.task.workflows
import djangobmf.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_task', '0003_changed_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='state',
            field=djangobmf.fields.WorkflowField(workflow=djangobmf.contrib.task.workflows.GoalWorkflow, max_length=32, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='state',
            field=djangobmf.fields.WorkflowField(workflow=djangobmf.contrib.task.workflows.TaskWorkflow, max_length=32, db_index=True),
            preserve_default=True,
        ),
    ]
