#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.utils.deprecation import RemovedInNextBMFVersionWarning

from djangobmf.workflow import State
from djangobmf.workflow import Transition
from djangobmf.workflow import Workflow
from djangobmf.workflow import DefaultWorkflow

import warnings


__all__ = [
    'State',
    'Transition',
    'Workflow',
    'DefaultWorkflow',
]

warnings.warn(
    "This djangobmf.workflows is deprecated, please use djangobmf.workflow",
    RemovedInNextBMFVersionWarning, stacklevel=2)
