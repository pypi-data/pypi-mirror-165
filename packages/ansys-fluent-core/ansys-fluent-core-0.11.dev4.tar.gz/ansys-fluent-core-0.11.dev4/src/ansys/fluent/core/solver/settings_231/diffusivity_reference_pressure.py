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
class diffusivity_reference_pressure(Group):
    """
    'diffusivity_reference_pressure' child.
    """

    fluent_name = "diffusivity-reference-pressure"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of diffusivity_reference_pressure.
    """
    option: option = option
    """
    option child of diffusivity_reference_pressure.
    """
    var_class: var_class = var_class
    """
    var_class child of diffusivity_reference_pressure.
    """
