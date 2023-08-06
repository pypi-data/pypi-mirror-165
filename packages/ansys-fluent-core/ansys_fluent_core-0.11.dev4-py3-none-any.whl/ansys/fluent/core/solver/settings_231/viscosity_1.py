#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .sutherland import sutherland
from .power_law import power_law
from .expression import expression
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['user_defined_function', 'sutherland', 'power_law', 'expression',
         'polynomial', 'piecewise_polynomial', 'piecewise_linear', 'value',
         'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of viscosity.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of viscosity.
    """
    power_law: power_law = power_law
    """
    power_law child of viscosity.
    """
    expression: expression = expression
    """
    expression child of viscosity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of viscosity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of viscosity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of viscosity.
    """
    value: value = value
    """
    value child of viscosity.
    """
    option: option = option
    """
    option child of viscosity.
    """
    var_class: var_class = var_class
    """
    var_class child of viscosity.
    """
