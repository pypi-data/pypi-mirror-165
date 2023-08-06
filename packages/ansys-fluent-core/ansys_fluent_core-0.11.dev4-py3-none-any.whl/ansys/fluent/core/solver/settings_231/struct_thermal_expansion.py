#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .orthotropic_structure_te import orthotropic_structure_te
from .value import value
from .option_8 import option
from .var_class import var_class
class struct_thermal_expansion(Group):
    """
    'struct_thermal_expansion' child.
    """

    fluent_name = "struct-thermal-expansion"

    child_names = \
        ['orthotropic_structure_te', 'value', 'option', 'var_class']

    orthotropic_structure_te: orthotropic_structure_te = orthotropic_structure_te
    """
    orthotropic_structure_te child of struct_thermal_expansion.
    """
    value: value = value
    """
    value child of struct_thermal_expansion.
    """
    option: option = option
    """
    option child of struct_thermal_expansion.
    """
    var_class: var_class = var_class
    """
    var_class child of struct_thermal_expansion.
    """
