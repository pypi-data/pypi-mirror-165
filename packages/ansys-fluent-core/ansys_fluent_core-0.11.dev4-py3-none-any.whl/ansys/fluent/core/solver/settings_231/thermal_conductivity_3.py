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
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of thermal_conductivity.
    """
    option: option = option
    """
    option child of thermal_conductivity.
    """
    var_class: var_class = var_class
    """
    var_class child of thermal_conductivity.
    """
