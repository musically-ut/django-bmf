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
)

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
    pass


class Configuration(AbstractConfiguration):
    pass


class Dashboard(AbstractDashboard):
    pass


class Document(AbstractDocument):
    pass


class Notification(AbstractNotification):
    pass


class NumberCycle(AbstractNumberCycle):
    pass


class Report(AbstractReport):
    pass
