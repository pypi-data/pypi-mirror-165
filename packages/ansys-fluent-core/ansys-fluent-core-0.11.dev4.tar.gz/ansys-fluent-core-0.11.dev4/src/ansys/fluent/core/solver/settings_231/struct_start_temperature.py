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
class struct_start_temperature(Group):
    """
    'struct_start_temperature' child.
    """

    fluent_name = "struct-start-temperature"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of struct_start_temperature.
    """
    option: option = option
    """
    option child of struct_start_temperature.
    """
    var_class: var_class = var_class
    """
    var_class child of struct_start_temperature.
    """
