#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

__all__ = (
    'BMFModel',
    'BMFModelMPTT',
    'ACTION_COMMENT',
    'ACTION_CREATED',
    'ACTION_UPDATED',
    'ACTION_WORKFLOW',
    'ACTION_FILE',
    'Activity',
    'Dashboard',
    'Document',
    'Configuration',
    'Notification',
    'NumberCycle',
    'Report',
    'Serializer',
)

from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import signals
from django.dispatch import receiver

from djangobmf.core.serializer import Serializer
from djangobmf.settings import APP_LABEL
from djangobmf.signals import activity_create
from djangobmf.signals import activity_update
from djangobmf.signals import activity_addfile
from djangobmf.signals import activity_workflow
from djangobmf.tasks import djangobmf_user_watch

import json

from .base import BMFModel
from .base import BMFModelMPTT

from .activity import ACTION_COMMENT
from .activity import ACTION_CREATED
from .activity import ACTION_UPDATED
from .activity import ACTION_WORKFLOW
from .activity import ACTION_FILE

from .activity import Activity as AbstractActivity
from .configuration import Configuration as AbstractConfiguration
from .dashboard import Dashboard as AbstractDashboard
from .document import Document as AbstractDocument
from .notification import Notification as AbstractNotification
from .numbering import NumberCycle as AbstractNumberCycle
from .report import Report as AbstractReport


class Activity(AbstractActivity):
    class Meta(AbstractActivity.Meta):
        abstract = False
        app_label = APP_LABEL


class Configuration(AbstractConfiguration):
    class Meta(AbstractConfiguration.Meta):
        abstract = False
        app_label = APP_LABEL


class Dashboard(AbstractDashboard):
    class Meta(AbstractDashboard.Meta):
        abstract = False
        app_label = APP_LABEL


class Document(AbstractDocument):
    class Meta(AbstractDocument.Meta):
        abstract = False
        app_label = APP_LABEL


class Notification(AbstractNotification):
    class Meta(AbstractNotification.Meta):
        abstract = False
        app_label = APP_LABEL


class NumberCycle(AbstractNumberCycle):
    class Meta(AbstractNumberCycle.Meta):
        abstract = False
        app_label = APP_LABEL


class Report(AbstractReport):
    class Meta(AbstractReport.Meta):
        abstract = False
        app_label = APP_LABEL


@receiver(activity_create)
def object_created(sender, instance, **kwargs):
    if instance._bmfmeta.has_history:
        history = Activity(
            user=instance.created_by,
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
            action=ACTION_CREATED,
        )
        history.save()


@receiver(activity_update)
def object_changed(sender, instance, **kwargs):
    if instance._bmfmeta.has_history and len(instance._bmfmeta.observed_fields) > 0:
        changes = []
        values = instance._get_observed_values()
        for key in instance._bmfmeta.observed_fields:
            try:
                if instance._bmfmeta.changelog[key] != values[key]:
                    changes.append((key, instance._bmfmeta.changelog[key], values[key]))
            except KeyError:
                pass
        if len(changes) > 0:
            history = Activity(
                user=instance.modified_by,
                parent_ct=ContentType.objects.get_for_model(sender),
                parent_id=instance.pk,
                action=ACTION_UPDATED,
                text=json.dumps(changes, cls=DjangoJSONEncoder),
            )
            history.save()


@receiver(activity_workflow)
def new_state(sender, instance, **kwargs):
    if instance._bmfmeta.has_history:
        history = Activity(
            user=instance.modified_by,
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
            action=ACTION_WORKFLOW,
            text=json.dumps({
                'old': instance._bmfworkflow._initial_state_key,
                'new': instance._bmfworkflow._current_state_key,
            }, cls=DjangoJSONEncoder),
        )
        history.save()


@receiver(activity_addfile)
def new_file(sender, instance, file, **kwargs):
    if instance._bmfmeta.has_history:
        history = Activity(
            user=instance.modified_by,
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
            action=ACTION_FILE,
            text=json.dumps({
                'pk': file.pk,
                'size': file.size,
                'name': '%s' % file,
            }, cls=DjangoJSONEncoder),
        )
        history.save()


def activity_post_save(sender, instance, *args, **kwargs):
    djangobmf_user_watch(instance.pk)
signals.post_save.connect(activity_post_save, sender=Activity)
