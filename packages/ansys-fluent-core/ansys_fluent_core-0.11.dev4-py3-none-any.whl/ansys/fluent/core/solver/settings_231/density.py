#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .rgp_table import rgp_table
from .user_defined_function import user_defined_function
from .expression import expression
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .compressible_liquid import compressible_liquid
from .value import value
from .real_gas_nist import real_gas_nist
from .option_8 import option
from .var_class import var_class
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['rgp_table', 'user_defined_function', 'expression', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'compressible_liquid',
         'value', 'real_gas_nist', 'option', 'var_class']

    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of density.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of density.
    """
    expression: expression = expression
    """
    expression child of density.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of density.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of density.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of density.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of density.
    """
    value: value = value
    """
    value child of density.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of density.
    """
    option: option = option
    """
    option child of density.
    """
    var_class: var_class = var_class
    """
    var_class child of density.
    """
