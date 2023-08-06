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
class degrees_of_freedom(Group):
    """
    'degrees_of_freedom' child.
    """

    fluent_name = "degrees-of-freedom"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of degrees_of_freedom.
    """
    option: option = option
    """
    option child of degrees_of_freedom.
    """
    var_class: var_class = var_class
    """
    var_class child of degrees_of_freedom.
    """
