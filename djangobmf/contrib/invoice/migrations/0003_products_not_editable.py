# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_invoice', '0002_remove_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='products',
            field=models.ManyToManyField(through='djangobmf_invoice.InvoiceProduct', to=settings.BMF_CONTRIB_PRODUCT, editable=False),
            preserve_default=True,
        ),
    ]
