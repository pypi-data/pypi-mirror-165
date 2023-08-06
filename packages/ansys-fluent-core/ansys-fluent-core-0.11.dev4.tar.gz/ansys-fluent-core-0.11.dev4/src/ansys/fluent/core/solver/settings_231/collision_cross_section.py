#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_8 import option
from .var_class import var_class
class collision_cross_section(Group):
    """
    'collision_cross_section' child.
    """

    fluent_name = "collision-cross-section"

    child_names = \
        ['option', 'var_class']

    option: option = option
    """
    option child of collision_cross_section.
    """
    var_class: var_class = var_class
    """
    var_class child of collision_cross_section.
    """
