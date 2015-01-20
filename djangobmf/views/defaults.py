#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def bad_request(request):
    """
    400 error handler.
    """
    template = get_template("djangobmf/400.html")
    return HttpResponseBadRequest(
        template.render(
            Context({})
        )
    )


@requires_csrf_token
def permission_denied(request):
    """
    403 error handler.
    """
    template = get_template("djangobmf/403.html")
    return HttpResponseForbidden(
        template.render(
            RequestContext(request)
        )
    )


@requires_csrf_token
def page_not_found(request):
    """
    404 handler.
    """
    template = get_template("djangobmf/404.html")
    return HttpResponseNotFound(
        template.render(
            RequestContext(request)
        )
    )


@requires_csrf_token
def server_error(request):
    """
    500 error handler.
    """
    template = get_template("djangobmf/500.html")
    return HttpResponseServerError(
        template.render(
            Context({})
        )
    )
