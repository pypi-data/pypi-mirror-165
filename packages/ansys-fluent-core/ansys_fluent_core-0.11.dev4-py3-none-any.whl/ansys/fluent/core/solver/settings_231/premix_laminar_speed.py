#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .combustion_mixture import combustion_mixture
from .user_defined_function import user_defined_function
from .value import value
from .option_8 import option
from .var_class import var_class
class premix_laminar_speed(Group):
    """
    'premix_laminar_speed' child.
    """

    fluent_name = "premix-laminar-speed"

    child_names = \
        ['combustion_mixture', 'user_defined_function', 'value', 'option',
         'var_class']

    combustion_mixture: combustion_mixture = combustion_mixture
    """
    combustion_mixture child of premix_laminar_speed.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_laminar_speed.
    """
    value: value = value
    """
    value child of premix_laminar_speed.
    """
    option: option = option
    """
    option child of premix_laminar_speed.
    """
    var_class: var_class = var_class
    """
    var_class child of premix_laminar_speed.
    """
