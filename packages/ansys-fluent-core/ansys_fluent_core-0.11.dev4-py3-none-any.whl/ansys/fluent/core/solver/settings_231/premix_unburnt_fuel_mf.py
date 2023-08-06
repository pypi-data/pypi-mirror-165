#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .value import value
from .option_8 import option
from .var_class import var_class
class premix_unburnt_fuel_mf(Group):
    """
    'premix_unburnt_fuel_mf' child.
    """

    fluent_name = "premix-unburnt-fuel-mf"

    child_names = \
        ['user_defined_function', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_unburnt_fuel_mf.
    """
    value: value = value
    """
    value child of premix_unburnt_fuel_mf.
    """
    option: option = option
    """
    option child of premix_unburnt_fuel_mf.
    """
    var_class: var_class = var_class
    """
    var_class child of premix_unburnt_fuel_mf.
    """
