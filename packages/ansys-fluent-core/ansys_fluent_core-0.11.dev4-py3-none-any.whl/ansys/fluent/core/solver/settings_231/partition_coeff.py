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
class partition_coeff(Group):
    """
    'partition_coeff' child.
    """

    fluent_name = "partition-coeff"

    child_names = \
        ['user_defined_function', 'polynomial', 'piecewise_polynomial',
         'piecewise_linear', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of partition_coeff.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of partition_coeff.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of partition_coeff.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of partition_coeff.
    """
    value: value = value
    """
    value child of partition_coeff.
    """
    option: option = option
    """
    option child of partition_coeff.
    """
    var_class: var_class = var_class
    """
    var_class child of partition_coeff.
    """
