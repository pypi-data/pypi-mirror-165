#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_8 import option
from .var_class import var_class
class scattering_factor(Group):
    """
    'scattering_factor' child.
    """

    fluent_name = "scattering-factor"

    child_names = \
        ['option', 'var_class']

    option: option = option
    """
    option child of scattering_factor.
    """
    var_class: var_class = var_class
    """
    var_class child of scattering_factor.
    """
