#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .value import value
from .user_defined_function import user_defined_function
from .option_8 import option
from .var_class import var_class
class specific_heat(Group):
    """
    'specific_heat' child.
    """

    fluent_name = "specific-heat"

    child_names = \
        ['value', 'user_defined_function', 'option', 'var_class']

    value: value = value
    """
    value child of specific_heat.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of specific_heat.
    """
    option: option = option
    """
    option child of specific_heat.
    """
    var_class: var_class = var_class
    """
    var_class child of specific_heat.
    """
