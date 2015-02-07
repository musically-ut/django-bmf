# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields
import djangobmf.contrib.timesheet.workflows


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_timesheet', '0005_changed_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='state',
            field=djangobmf.fields.WorkflowField(workflow=djangobmf.contrib.timesheet.workflows.TimesheetWorkflow, max_length=32, db_index=True),
            preserve_default=True,
        ),
    ]
