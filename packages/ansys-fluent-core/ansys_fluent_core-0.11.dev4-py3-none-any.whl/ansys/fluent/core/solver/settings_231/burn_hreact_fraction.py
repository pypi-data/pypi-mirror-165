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
class burn_hreact_fraction(Group):
    """
    'burn_hreact_fraction' child.
    """

    fluent_name = "burn-hreact-fraction"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of burn_hreact_fraction.
    """
    option: option = option
    """
    option child of burn_hreact_fraction.
    """
    var_class: var_class = var_class
    """
    var_class child of burn_hreact_fraction.
    """
