#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .value import value
from .vibrational_modes import vibrational_modes
from .option_8 import option
from .var_class import var_class
class characteristic_vibrational_temperature(Group):
    """
    'characteristic_vibrational_temperature' child.
    """

    fluent_name = "characteristic-vibrational-temperature"

    child_names = \
        ['value', 'vibrational_modes', 'option', 'var_class']

    value: value = value
    """
    value child of characteristic_vibrational_temperature.
    """
    vibrational_modes: vibrational_modes = vibrational_modes
    """
    vibrational_modes child of characteristic_vibrational_temperature.
    """
    option: option = option
    """
    option child of characteristic_vibrational_temperature.
    """
    var_class: var_class = var_class
    """
    var_class child of characteristic_vibrational_temperature.
    """
