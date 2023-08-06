#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .expression import expression
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class saturation_pressure(Group):
    """
    'saturation_pressure' child.
    """

    fluent_name = "saturation-pressure"

    child_names = \
        ['user_defined_function', 'expression', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'value', 'option',
         'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of saturation_pressure.
    """
    expression: expression = expression
    """
    expression child of saturation_pressure.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of saturation_pressure.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of saturation_pressure.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of saturation_pressure.
    """
    value: value = value
    """
    value child of saturation_pressure.
    """
    option: option = option
    """
    option child of saturation_pressure.
    """
    var_class: var_class = var_class
    """
    var_class child of saturation_pressure.
    """
