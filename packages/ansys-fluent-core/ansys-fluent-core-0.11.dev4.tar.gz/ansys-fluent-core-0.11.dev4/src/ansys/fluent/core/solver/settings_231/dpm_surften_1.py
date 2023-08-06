#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .rgp_table import rgp_table
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class dpm_surften(Group):
    """
    'dpm_surften' child.
    """

    fluent_name = "dpm-surften"

    child_names = \
        ['user_defined_function', 'rgp_table', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'value', 'option',
         'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of dpm_surften.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of dpm_surften.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of dpm_surften.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of dpm_surften.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of dpm_surften.
    """
    value: value = value
    """
    value child of dpm_surften.
    """
    option: option = option
    """
    option child of dpm_surften.
    """
    var_class: var_class = var_class
    """
    var_class child of dpm_surften.
    """
