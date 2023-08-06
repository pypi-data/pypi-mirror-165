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
class combustible_fraction(Group):
    """
    'combustible_fraction' child.
    """

    fluent_name = "combustible-fraction"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of combustible_fraction.
    """
    option: option = option
    """
    option child of combustible_fraction.
    """
    var_class: var_class = var_class
    """
    var_class child of combustible_fraction.
    """
