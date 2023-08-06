#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_4 import set
from .enable_9 import enable
class conjugate_heat_transfer(Group):
    """
    'conjugate_heat_transfer' child.
    """

    fluent_name = "conjugate-heat-transfer"

    child_names = \
        ['set']

    set: set = set
    """
    set child of conjugate_heat_transfer.
    """
    command_names = \
        ['enable']

    enable: enable = enable
    """
    enable command of conjugate_heat_transfer.
    """
