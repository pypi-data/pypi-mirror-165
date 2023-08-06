#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .orthotropic_structure_ym import orthotropic_structure_ym
from .value import value
from .option_8 import option
from .var_class import var_class
class struct_youngs_modulus(Group):
    """
    'struct_youngs_modulus' child.
    """

    fluent_name = "struct-youngs-modulus"

    child_names = \
        ['orthotropic_structure_ym', 'value', 'option', 'var_class']

    orthotropic_structure_ym: orthotropic_structure_ym = orthotropic_structure_ym
    """
    orthotropic_structure_ym child of struct_youngs_modulus.
    """
    value: value = value
    """
    value child of struct_youngs_modulus.
    """
    option: option = option
    """
    option child of struct_youngs_modulus.
    """
    var_class: var_class = var_class
    """
    var_class child of struct_youngs_modulus.
    """
