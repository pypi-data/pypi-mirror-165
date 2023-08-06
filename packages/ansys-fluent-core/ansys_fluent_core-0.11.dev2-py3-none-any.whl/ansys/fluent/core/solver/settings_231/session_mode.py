#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .process_count import process_count
from .host_name import host_name
class session_mode(Group):
    """
    Setup helper session for multidomain conjugate heat transfer.
    """

    fluent_name = "session-mode"

    child_names = \
        ['process_count', 'host_name']

    process_count: process_count = process_count
    """
    process_count child of session_mode.
    """
    host_name: host_name = host_name
    """
    host_name child of session_mode.
    """
