#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from .models import Product


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        exclude = []


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        exclude = []
