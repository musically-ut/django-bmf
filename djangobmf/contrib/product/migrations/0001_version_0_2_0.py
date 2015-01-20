# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('djangobmf_product', '0001_initial'), ('djangobmf_product', '0002_version_0_2_0')]

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_TAX),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.BMF_CONTRIB_ACCOUNT),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(verbose_name='UUID', blank=True, max_length=100, null=True, db_index=True, editable=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('code', models.CharField(verbose_name='Product Code', blank=True, db_index=True, max_length=255)),
                ('type', models.PositiveSmallIntegerField(verbose_name='Product type', choices=[(1, 'Service')], default=1)),
                ('can_sold', models.BooleanField(verbose_name='Can be sold', default=False, db_index=True)),
                ('can_purchased', models.BooleanField(verbose_name='Can be purchased', default=False, db_index=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('price_currency', djangobmf.fields.CurrencyField(max_length=4, editable=False)),
                ('price_precision', models.PositiveSmallIntegerField(default=0, null=True, blank=True, editable=False)),
                ('price', djangobmf.fields.MoneyField(verbose_name='Price', default='0', blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, null=True, blank=True, editable=False)),
                ('expense_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_expense', to=settings.BMF_CONTRIB_ACCOUNT)),
                ('income_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_income', to=settings.BMF_CONTRIB_ACCOUNT)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, null=True, blank=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
                'abstract': False,
                'ordering': ['name'],
                'swappable': 'BMF_CONTRIB_PRODUCT',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductTax',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('included', models.BooleanField(verbose_name='Is the tax included in the price?', default=False)),
                ('product', models.ForeignKey(related_name='product_tax', null=True, blank=True, to=settings.BMF_CONTRIB_PRODUCT)),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_tax', null=True, blank=True, to=settings.BMF_CONTRIB_TAX)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='producttax',
            unique_together=set([('product', 'tax')]),
        ),
        migrations.AddField(
            model_name='product',
            name='taxes',
            field=models.ManyToManyField(through='djangobmf_product.ProductTax', related_name='product_taxes', blank=True, to=settings.BMF_CONTRIB_TAX),
            preserve_default=True,
        ),
    ]
