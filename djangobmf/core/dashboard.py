#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


class Dashboard(object):
    name = None
    slug = None

    def __init__(self, *args):
        # TODO add validation
        # if not self.name or not name self.slug:
        #     raise

        self.data = args
