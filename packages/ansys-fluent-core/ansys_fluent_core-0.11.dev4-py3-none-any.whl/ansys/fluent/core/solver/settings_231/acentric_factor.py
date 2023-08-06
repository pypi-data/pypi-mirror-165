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
class acentric_factor(Group):
    """
    'acentric_factor' child.
    """

    fluent_name = "acentric-factor"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of acentric_factor.
    """
    option: option = option
    """
    option child of acentric_factor.
    """
    var_class: var_class = var_class
    """
    var_class child of acentric_factor.
    """
