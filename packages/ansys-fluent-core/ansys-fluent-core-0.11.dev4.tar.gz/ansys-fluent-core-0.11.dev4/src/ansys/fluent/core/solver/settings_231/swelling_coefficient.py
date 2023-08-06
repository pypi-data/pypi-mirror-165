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
class swelling_coefficient(Group):
    """
    'swelling_coefficient' child.
    """

    fluent_name = "swelling-coefficient"

    child_names = \
        ['user_defined_function', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of swelling_coefficient.
    """
    value: value = value
    """
    value child of swelling_coefficient.
    """
    option: option = option
    """
    option child of swelling_coefficient.
    """
    var_class: var_class = var_class
    """
    var_class child of swelling_coefficient.
    """
