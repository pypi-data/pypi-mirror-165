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
class thermophoretic_co(Group):
    """
    'thermophoretic_co' child.
    """

    fluent_name = "thermophoretic-co"

    child_names = \
        ['user_defined_function', 'polynomial', 'piecewise_polynomial',
         'piecewise_linear', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermophoretic_co.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of thermophoretic_co.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermophoretic_co.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermophoretic_co.
    """
    value: value = value
    """
    value child of thermophoretic_co.
    """
    option: option = option
    """
    option child of thermophoretic_co.
    """
    var_class: var_class = var_class
    """
    var_class child of thermophoretic_co.
    """
