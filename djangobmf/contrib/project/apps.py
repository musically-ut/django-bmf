from __future__ import unicode_literals

# from django.utils.translation import ugettext_lazy as _

from djangobmf.apps import ContribTemplate
# from djangobmf.categories import BaseCategory
# from djangobmf.categories import ProjectManagement


# class ProjectCategory(BaseCategory):
#     name = _('Projects')
#     slug = "projects"


class ProjectConfig(ContribTemplate):
    name = 'djangobmf.contrib.project'
    label = "djangobmf_project"

#   bmf_views = {
#       ProjectManagement(
#           ProjectCategory(
#               active={
#                   'model': "Project",
#                   'name': _("Active Projects"),
#                   'manager': "active",
#               },
#               all={
#                   'model': "Project",
#                   'name': _("All Projects"),
#               },
#           ),
#       ),
#   }
