#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.decorators.cache import never_cache
from django.views.defaults import permission_denied

from djangobmf import get_version
from djangobmf.decorators import login_required
from djangobmf.document.forms import UploadDocument
from djangobmf.notification.forms import HistoryCommentForm
from djangobmf.models import Activity
from djangobmf.models import Document
from djangobmf.models import Notification
from djangobmf.utils.serializers import DjangoBMFEncoder
from djangobmf.utils.user import user_add_bmf
from djangobmf.settings import APP_LABEL

import json
import datetime
import re
try:
    from urllib import parse
except ImportError:
    import urlparse as parse

import logging
logger = logging.getLogger(__name__)


class BaseMixin(object):
    """
    provides functionality used in EVERY view throughout the application.
    this is used so we don't neet to define a middleware
    """
    permissions = []

    def get_permissions(self, permissions=[]):
        """
        returns a list of (django) permissions and use them in dispatch to
        determinate if the user can view the page, he requested
        """
        for perm in self.permissions:
            permissions.append(perm)
        return permissions

    def check_permissions(self):
        """
        overwrite this function to add a view permission check (i.e
        one which depends on the object or on the request)
        """
        return True

    def read_session_data(self):
        return self.request.session.get("djangobmf", {'version': get_version()})

    def write_session_data(self, data):
        # reload sessiondata, because we can not be sure, that the
        # session was not changed during this request
        session_data = self.read_session_data()
        session_data.update(data)

        # update session
        self.request.session["djangobmf"] = session_data
        self.request.session.modified = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        checks permissions, requires a login and
        because we are using a generic view approach to the data-models
        in django BMF, we can ditch a middleware (less configuration)
        and add the functionality to this function.
        """

        if not self.check_permissions() or not self.request.user.has_perms(self.get_permissions([])):
            return permission_denied(self.request)

        # === DJANGO BMF SITE OBJECT ======================================

        self.request.djangobmf_site = apps.get_app_config(APP_LABEL).site

        # === EMPLOYEE AND TEAMS ==========================================

        # automagicaly add the authenticated user and employee to the request (as a lazy queryset)
        user_add_bmf(self.request.user)

        if self.request.user.djangobmf_has_employee and not self.request.user.djangobmf_employee:
            logger.debug("User %s does not have permission to access djangobmf" % self.request.user)
            if self.request.user.is_superuser:
                return redirect('djangobmf:wizard', permanent=False)
            else:
                raise PermissionDenied

        # =================================================================

        response = super(BaseMixin, self).dispatch(*args, **kwargs)

        if response.status_code in [400, 404, 403, 405, 500] and not settings.DEBUG:
            # Catch HTTP error codes and redirect to a bmf-specific template
            # * 400 Bad Request
            # * 404 Not Found
            # * 403 Forbidden
            # * 405 Not allowed
            # * 500 Server Error
            # TODO
            logger.debug("TESTING RESPONSE %s" % response.status_code)

        return response

    def update_workspace(self, dashboard=None):
        """
        This function reads all workspaces for a user instance, builds the
        navigation-tree and updates the active workspace (if neccessary)

        workspace can either be None, the dashboards key or None
        """
        workspace = dashboard  # TODO: OLD

        cache_key = 'bmf_workspace_%s_%s' % (self.request.user.pk, get_language())
        cache_timeout = 600

        # get navigation key from cache
        data = cache.get(cache_key)
        if not data:  # pragma: no branch
            logger.debug("Reload workspace cache (%s) for user %s" % (cache_key, self.request.user))

            data = {
                "relations": {},
                "dashboards": {},
                "workspace": {},
            }

            cache.set(cache_key, data, cache_timeout)

        db, cat = data['relations'].get(workspace, (None, None))
        if cat:
            view = data['workspace'][db]["categories"][cat]["views"][workspace]
        else:
            view = None

        if not db:
            return data["dashboards"], None, None, None, None
        return data["dashboards"], data["workspace"][db], db, workspace, view

    def update_notification(self, count=None):
        """
        This function is used by django BMF to update the notifications
        used in the BMF-Framework
        """
        logger.debug("Updating notifications for %s" % self.request.user)

        # get all session data
        session_data = self.read_session_data()

        # manipulate session
        session_data["notification_last_update"] = datetime.datetime.utcnow().isoformat()
        if count is None:
            session_data["notification_count"] = Notification.objects.filter(
                unread=True,
                user=self.request.user,
            ).count()
        else:
            session_data["notification_count"] = count

        # update session
        self.write_session_data(session_data)


class ViewMixin(BaseMixin):

    def get_context_data(self, **kwargs):

        session_data = self.read_session_data()

        # load the current workspace
        dashboards, workspace, db_active, ws_active, ws_view = self.update_workspace(
            getattr(self, 'workspace', session_data.get('workspace', None))
        )

        # update session
        if db_active and ws_active and session_data.get('dashboard') != db_active \
                or db_active != ws_active and session_data.get('workspace') != ws_active:
            logger.debug("Update session for %s: (dashboard %s->%s) (workspace %s->%s)" % (
                self.request.user,
                session_data.get('dashboard', None),
                db_active,
                session_data.get('workspace', None),
                ws_active,
            ))
            session_data['dashboard'] = db_active
            session_data['workspace'] = ws_active
            self.write_session_data(session_data)

        # update context with session data
        kwargs.update({
            'djangobmf': self.read_session_data(),
            'bmfworkspace': {
                'dashboards': dashboards,
                'workspace': workspace,
                'workspace_active': session_data.get('dashboard', None),
                'dashboard_active': session_data.get('workspace', None),
            },
        })

        # always read current version, if in development mode
        if settings.DEBUG:
            kwargs["djangobmf"]['version'] = get_version()

        return super(ViewMixin, self).get_context_data(**kwargs)


class AjaxMixin(BaseMixin):
    """
    add some basic function for ajax requests
    """
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(AjaxMixin, self).dispatch(*args, **kwargs)

    def check_permissions(self):
        return self.request.is_ajax() and super(AjaxMixin, self).check_permissions()

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=DjangoBMFEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get_ajax_context(self, context):
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(AjaxMixin, self).render_to_response(context, **response_kwargs)
        response.render()
        ctx = self.get_ajax_context({
            'html': response.rendered_content,
        })
        return self.render_to_json_response(ctx)

    def render_valid_form(self, context):
        ctx = self.get_ajax_context({
            'status': 'valid',
        })
        ctx.update(context)
        return self.render_to_json_response(ctx)


class NextMixin(object):
    """
    redirects to an url or to next, if it is set via get
    """

    def redirect_next(self, reverse=None, *args, **kwargs):
        if 'next' in self.request.REQUEST:
            redirect_to = self.request.REQUEST.get('next', '')

            netloc = parse.urlparse(redirect_to)[1]
            if not netloc or netloc == self.request.get_host():
                return redirect_to

        if hasattr(self, 'success_url') and self.success_url:
            return self.success_url

        if reverse:
            return reverse_lazy(reverse, args=args, kwargs=kwargs)

        return self.request.path_info


# PERMISSIONS

class ModuleViewPermissionMixin(object):
    """
    Checks view permissions of an bmfmodule
    """

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.view_%s' % info)
        return super(ModuleViewPermissionMixin, self).get_permissions(perms)


class ModuleCreatePermissionMixin(object):
    """
    Checks create permissions of an bmfmodule
    """

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.add_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleCreatePermissionMixin, self).get_permissions(perms)


class ModuleClonePermissionMixin(object):
    """
    Checks create permissions of an bmfmodule
    """

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.clone_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleClonePermissionMixin, self).get_permissions(perms)


class ModuleUpdatePermissionMixin(object):
    """
    Checks update permissions of an bmfmodule
    """

    def check_permissions(self):
        return self.get_object()._bmfworkflow._current_state.update \
            and super(ModuleUpdatePermissionMixin, self).check_permissions()

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.change_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleUpdatePermissionMixin, self).get_permissions(perms)


class ModuleDeletePermissionMixin(object):
    """
    Checks delete permission of an bmfmodule
    """

    def check_permissions(self):
        return self.get_object()._bmfworkflow._current_state.delete \
            and super(ModuleDeletePermissionMixin, self).check_permissions()

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.delete_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleDeletePermissionMixin, self).get_permissions(perms)


# MODULES

class ModuleBaseMixin(object):
    model = None

    def get_queryset(self, manager=None):
        """
        Return the list of items for this view.
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.model and manager and hasattr(self.model._default_manager, manager):
            qs = getattr(self.model._default_manager, manager)(self.request)
        elif self.model is not None:
            qs = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model " % {
                    'cls': self.__class__.__name__
                }
            )

#       return qs

#   def get_queryset(self):
#       if self.queryset is not None:
#           queryset = self.queryset
#           if isinstance(queryset, QuerySet):
#               queryset = queryset.all()
#       elif self.model is not None:
#           queryset = self.model._default_manager.all()
#       else:
#           raise ImproperlyConfigured(
#               "%(cls)s is missing a QuerySet. Define "
#               "%(cls)s.model, %(cls)s.queryset, or override "
#               "%(cls)s.get_queryset()." % {
#                   'cls': self.__class__.__name__
#               }
#           )

        # load employee and team data into user
        user_add_bmf(self.request.user)

        return self.model.has_permissions(qs, self.request.user)

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        return super(ModuleBaseMixin, self).get_object()

    def get_context_data(self, **kwargs):
        info = self.model._meta.app_label, self.model._meta.model_name
        kwargs.update({
            'bmfmodule': {
                'verbose_name_plural': self.model._meta.verbose_name_plural,
                'create_views': self.model._bmfmeta.create_views,
                'model': self.model,
                # 'contenttype': ContentType.objects.get_for_model(self.model).pk,
                'has_report': self.model._bmfmeta.has_report,
                'can_clone': self.model._bmfmeta.can_clone and self.request.user.has_perms([
                    '%s.view_%s' % info,
                    '%s.clone_%s' % info,
                ]),
                # 'verbose_name': self.model._meta.verbose_name,  # unused
            },
        })
        if hasattr(self, 'object') and self.object:
            kwargs.update({
                'bmfworkflow': {
                    'enabled': bool(len(self.model._bmfworkflow._transitions)),
                    'state': self.object._bmfworkflow._current_state,
                    'transitions': self.object._bmfworkflow._from_here(self.object, self.request.user),
                },
            })
        return super(ModuleBaseMixin, self).get_context_data(**kwargs)


class ModuleAjaxMixin(ModuleBaseMixin, AjaxMixin):
    """
    base mixin for update, clone and create views (ajax-forms)
    and form-api
    """

    def get_ajax_context(self, context):
        ctx = {
            'object_pk': 0,
            'status': 'ok',  # "ok" for normal html, "valid" for valid forms, "error" if an error occured
            'html': '',
            'message': '',
            'redirect': '',
        }
        ctx.update(context)
        return ctx

    def render_valid_form(self, context):
        context.update({
            'redirect': self.get_success_url(),
        })
        return super(ModuleAjaxMixin, self).render_valid_form(context)


class ModuleViewMixin(ModuleBaseMixin, ViewMixin):
    """
    Basic objects, includes bmf-specific functions and context
    variables for bmf-views
    """
    pass


class ModuleSearchMixin(object):
    """
    Adds the methods ``normalize_query`` and ``construct_search``
    """

    def normalize_query(
            self, query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
            normspace=re.compile(r'\s{2,}').sub):
        '''
        Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.

        Example:
        > self.normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    # Apply keyword searches.
    def construct_search(self, field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name


class ModuleActivityMixin(object):
    """
    Parse history to view (as a context variable)
    """

    def get_context_data(self, **kwargs):
        ct = ContentType.objects.get_for_model(self.object)

        try:
            watch = Notification.objects.get(
                user=self.request.user,
                watch_ct=ct,
                watch_id=self.object.pk
            )
            if watch.unread:
                watch.unread = False
                watch.save()
            notification = watch
            watching = watch.is_active()
        except Notification.DoesNotExist:
            notification = None
            watching = False

        kwargs.update({
            'bmfactivity': {
                'qs': Activity.objects.filter(parent_ct=ct, parent_id=self.object.pk),
                'enabled': (self.model._bmfmeta.has_comments or self.model._bmfmeta.has_history),
                'comments': self.model._bmfmeta.has_comments,
                'log': self.model._bmfmeta.has_history,
                'pk': self.object.pk,
                'ct': ct.pk,
                'notification': notification,
                'watch': watching,
                'log_data': None,
                'comment_form': None,
                'object_ct': ct,
                'object_pk': self.object.pk,
            },
        })
        if self.model._bmfmeta.has_history:
            kwargs['bmfactivity']['log_data'] = Activity.objects.select_related('user') \
                .filter(parent_ct=ct, parent_id=self.object.pk)
        if self.model._bmfmeta.has_comments:
            kwargs['bmfactivity']['comment_form'] = HistoryCommentForm()
        return super(ModuleActivityMixin, self).get_context_data(**kwargs)


class ModuleFilesMixin(object):
    """
    Parse files to view (as a context variable)
    """

    def get_context_data(self, **kwargs):
        if self.model._bmfmeta.has_files:
            ct = ContentType.objects.get_for_model(self.object)

            kwargs.update({
                'has_files': True,
                'history_file_form': UploadDocument,
                'files': Document.objects.filter(content_type=ct, content_id=self.object.pk),
            })
        return super(ModuleFilesMixin, self).get_context_data(**kwargs)


class ModuleFormMixin(object):
    """
    make an BMF-Form
    """
    fields = None
    exclude = []

    def get_form_class(self, *args, **kwargs):
        """
        Returns the form class to use in this view.
        """
        if not self.form_class:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model

            if isinstance(self.fields, list):
                self.form_class = modelform_factory(model, fields=self.fields)
            else:
                self.form_class = modelform_factory(model, exclude=self.exclude)
        return self.form_class
