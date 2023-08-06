#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .orthotropic_structure_nu import orthotropic_structure_nu
from .value import value
from .option_8 import option
from .var_class import var_class
class struct_poisson_ratio(Group):
    """
    'struct_poisson_ratio' child.
    """

    fluent_name = "struct-poisson-ratio"

    child_names = \
        ['orthotropic_structure_nu', 'value', 'option', 'var_class']

    orthotropic_structure_nu: orthotropic_structure_nu = orthotropic_structure_nu
    """
    orthotropic_structure_nu child of struct_poisson_ratio.
    """
    value: value = value
    """
    value child of struct_poisson_ratio.
    """
    option: option = option
    """
    option child of struct_poisson_ratio.
    """
    var_class: var_class = var_class
    """
    var_class child of struct_poisson_ratio.
    """
