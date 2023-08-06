#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .value import value
from .option_8 import option
from .var_class import var_class
class struct_damping_alpha(Group):
    """
    'struct_damping_alpha' child.
    """

    fluent_name = "struct-damping-alpha"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of struct_damping_alpha.
    """
    option: option = option
    """
    option child of struct_damping_alpha.
    """
    var_class: var_class = var_class
    """
    var_class child of struct_damping_alpha.
    """
