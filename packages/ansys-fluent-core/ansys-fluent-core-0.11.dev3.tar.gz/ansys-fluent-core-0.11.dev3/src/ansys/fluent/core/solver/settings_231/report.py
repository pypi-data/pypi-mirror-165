#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .simulation_reports import simulation_reports
from .report_menu import report_menu
class report(Group):
    """
    'report' child.
    """

    fluent_name = "report"

    child_names = \
        ['simulation_reports', 'report_menu']

    simulation_reports: simulation_reports = simulation_reports
    """
    simulation_reports child of report.
    """
    report_menu: report_menu = report_menu
    """
    report_menu child of report.
    """
