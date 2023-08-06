#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .real_gas_nist import real_gas_nist
from .rgp_table import rgp_table
from .user_defined_function import user_defined_function
from .expression import expression
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['real_gas_nist', 'rgp_table', 'user_defined_function', 'expression',
         'polynomial', 'piecewise_polynomial', 'piecewise_linear', 'value',
         'option', 'var_class']

    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of thermal_conductivity.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of thermal_conductivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermal_conductivity.
    """
    expression: expression = expression
    """
    expression child of thermal_conductivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of thermal_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermal_conductivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermal_conductivity.
    """
    value: value = value
    """
    value child of thermal_conductivity.
    """
    option: option = option
    """
    option child of thermal_conductivity.
    """
    var_class: var_class = var_class
    """
    var_class child of thermal_conductivity.
    """
