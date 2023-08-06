#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .rgp_table import rgp_table
from .value import value
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .option_8 import option
from .var_class import var_class
class vapor_pressure(Group):
    """
    'vapor_pressure' child.
    """

    fluent_name = "vapor-pressure"

    child_names = \
        ['user_defined_function', 'rgp_table', 'value', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of vapor_pressure.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of vapor_pressure.
    """
    value: value = value
    """
    value child of vapor_pressure.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of vapor_pressure.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of vapor_pressure.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of vapor_pressure.
    """
    option: option = option
    """
    option child of vapor_pressure.
    """
    var_class: var_class = var_class
    """
    var_class child of vapor_pressure.
    """
