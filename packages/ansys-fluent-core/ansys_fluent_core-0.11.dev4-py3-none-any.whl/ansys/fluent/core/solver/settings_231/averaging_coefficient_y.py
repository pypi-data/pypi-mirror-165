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
class averaging_coefficient_y(Group):
    """
    'averaging_coefficient_y' child.
    """

    fluent_name = "averaging-coefficient-y"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of averaging_coefficient_y.
    """
    option: option = option
    """
    option child of averaging_coefficient_y.
    """
    var_class: var_class = var_class
    """
    var_class child of averaging_coefficient_y.
    """
