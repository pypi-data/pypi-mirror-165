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
class charge_density(Group):
    """
    'charge_density' child.
    """

    fluent_name = "charge-density"

    child_names = \
        ['user_defined_function', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of charge_density.
    """
    value: value = value
    """
    value child of charge_density.
    """
    option: option = option
    """
    option child of charge_density.
    """
    var_class: var_class = var_class
    """
    var_class child of charge_density.
    """
