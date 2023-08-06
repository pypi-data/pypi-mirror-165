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
class lithium_diffusivity(Group):
    """
    'lithium_diffusivity' child.
    """

    fluent_name = "lithium-diffusivity"

    child_names = \
        ['user_defined_function', 'expression', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'value', 'option',
         'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of lithium_diffusivity.
    """
    expression: expression = expression
    """
    expression child of lithium_diffusivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of lithium_diffusivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of lithium_diffusivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of lithium_diffusivity.
    """
    value: value = value
    """
    value child of lithium_diffusivity.
    """
    option: option = option
    """
    option child of lithium_diffusivity.
    """
    var_class: var_class = var_class
    """
    var_class child of lithium_diffusivity.
    """
