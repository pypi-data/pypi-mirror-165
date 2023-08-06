#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_1 import type
from .frequency import frequency
from .interval_1 import interval
class single_session_coupling(Group):
    """
    'single_session_coupling' child.
    """

    fluent_name = "single-session-coupling"

    child_names = \
        ['type', 'frequency', 'interval']

    type: type = type
    """
    type child of single_session_coupling.
    """
    frequency: frequency = frequency
    """
    frequency child of single_session_coupling.
    """
    interval: interval = interval
    """
    interval child of single_session_coupling.
    """
