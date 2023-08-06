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
class magnetic_permeability(Group):
    """
    'magnetic_permeability' child.
    """

    fluent_name = "magnetic-permeability"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of magnetic_permeability.
    """
    option: option = option
    """
    option child of magnetic_permeability.
    """
    var_class: var_class = var_class
    """
    var_class child of magnetic_permeability.
    """
