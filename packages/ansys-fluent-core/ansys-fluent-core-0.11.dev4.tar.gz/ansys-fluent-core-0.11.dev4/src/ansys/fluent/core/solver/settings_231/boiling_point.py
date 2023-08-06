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
class boiling_point(Group):
    """
    'boiling_point' child.
    """

    fluent_name = "boiling-point"

    child_names = \
        ['user_defined_function', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of boiling_point.
    """
    value: value = value
    """
    value child of boiling_point.
    """
    option: option = option
    """
    option child of boiling_point.
    """
    var_class: var_class = var_class
    """
    var_class child of boiling_point.
    """
