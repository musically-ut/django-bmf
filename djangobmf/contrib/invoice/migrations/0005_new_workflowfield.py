# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields
import djangobmf.contrib.invoice.workflows


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_invoice', '0004_changed_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='state',
            field=djangobmf.fields.WorkflowFieldV2(workflow=djangobmf.contrib.invoice.workflows.InvoiceWorkflow, max_length=32, db_index=True),
            preserve_default=True,
        ),
    ]
