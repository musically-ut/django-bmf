#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import template
from django.utils.safestring import mark_safe

import markdown

from djangobmf.utils.markdown.checklist import ChecklistExtension
from djangobmf.utils.markdown.mentions import MentionExtension
from djangobmf.utils.markdown.urlize import UrlizeExtension
from djangobmf.utils.markdown.strikethrough import StrikeThroughExtension

register = template.Library()


@register.filter(name="bmfmarkup")
def markdown_filter(text):
    """
    """
    if not text:
        return ''
    return mark_safe(markdown.markdown(
        text,
        extensions=[
            UrlizeExtension(),
            StrikeThroughExtension(),
            ChecklistExtension(),
            MentionExtension(),
            'smart_strong',
            'sane_lists',
            'smarty',
            'fenced_code',
        ],
        output_format="html5",
        save_mode='escape',
        smart_emphasis=True,
        lazy_ol=True,
    ))
markdown_filter.is_safe = True
