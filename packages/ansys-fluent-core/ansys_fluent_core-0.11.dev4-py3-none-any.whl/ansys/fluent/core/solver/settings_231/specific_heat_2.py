#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class specific_heat(Group):
    """
    'specific_heat' child.
    """

    fluent_name = "specific-heat"

    child_names = \
        ['user_defined_function', 'nasa_9_piecewise_polynomial', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'value', 'option',
         'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of specific_heat.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of specific_heat.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of specific_heat.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of specific_heat.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of specific_heat.
    """
    value: value = value
    """
    value child of specific_heat.
    """
    option: option = option
    """
    option child of specific_heat.
    """
    var_class: var_class = var_class
    """
    var_class child of specific_heat.
    """
