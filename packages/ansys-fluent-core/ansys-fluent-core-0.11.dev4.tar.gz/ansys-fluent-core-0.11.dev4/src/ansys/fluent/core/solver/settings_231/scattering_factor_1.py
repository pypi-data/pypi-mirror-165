#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class scattering_factor(Group):
    """
    'scattering_factor' child.
    """

    fluent_name = "scattering-factor"

    child_names = \
        ['user_defined_function', 'polynomial', 'piecewise_polynomial',
         'piecewise_linear', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of scattering_factor.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of scattering_factor.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of scattering_factor.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of scattering_factor.
    """
    value: value = value
    """
    value child of scattering_factor.
    """
    option: option = option
    """
    option child of scattering_factor.
    """
    var_class: var_class = var_class
    """
    var_class child of scattering_factor.
    """
