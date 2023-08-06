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
class therm_exp_coeff(Group):
    """
    'therm_exp_coeff' child.
    """

    fluent_name = "therm-exp-coeff"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of therm_exp_coeff.
    """
    option: option = option
    """
    option child of therm_exp_coeff.
    """
    var_class: var_class = var_class
    """
    var_class child of therm_exp_coeff.
    """
