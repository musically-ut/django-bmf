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
    'Workspace',
)

from .base import BMFModel
from .base import BMFModelMPTT

from .activity import ACTION_COMMENT
from .activity import ACTION_CREATED
from .activity import ACTION_UPDATED
from .activity import ACTION_WORKFLOW
from .activity import ACTION_FILE
from .activity import Activity
from .configuration import Configuration
from .dashboard import Dashboard as AbstractDashboard
from .document import Document
from .notification import Notification
from .numbering import NumberCycle
from .report import Report
from .workspace import Workspace


class Dashboard(AbstractDashboard):
    pass
