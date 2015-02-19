#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


class Report(object):

    def __init__(self, options):
        self.options = options

    def get_default_options(self):
        raise NotImplementedError('You need to implement a get_default_options function')

    def get_output_formats(self):
        raise NotImplementedError('You need to implement a get_output_formats function')

    def render(self, request, context):
        """
        returns extension, mime_type, data or file_object
        """
        raise NotImplementedError('You need to implement a render function')
