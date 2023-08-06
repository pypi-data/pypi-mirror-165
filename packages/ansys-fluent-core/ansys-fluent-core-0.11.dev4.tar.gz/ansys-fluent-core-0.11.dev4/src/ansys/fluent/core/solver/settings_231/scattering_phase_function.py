#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .delta_eddington import delta_eddington
from .value import value
from .option_8 import option
from .var_class import var_class
class scattering_phase_function(Group):
    """
    'scattering_phase_function' child.
    """

    fluent_name = "scattering-phase-function"

    child_names = \
        ['user_defined_function', 'delta_eddington', 'value', 'option',
         'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of scattering_phase_function.
    """
    delta_eddington: delta_eddington = delta_eddington
    """
    delta_eddington child of scattering_phase_function.
    """
    value: value = value
    """
    value child of scattering_phase_function.
    """
    option: option = option
    """
    option child of scattering_phase_function.
    """
    var_class: var_class = var_class
    """
    var_class child of scattering_phase_function.
    """
