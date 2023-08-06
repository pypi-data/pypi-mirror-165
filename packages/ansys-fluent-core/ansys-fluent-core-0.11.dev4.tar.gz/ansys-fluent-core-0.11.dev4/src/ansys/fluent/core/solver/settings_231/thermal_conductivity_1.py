#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .anisotropic import anisotropic
from .principal_axes_values import principal_axes_values
from .orthotropic import orthotropic
from .cyl_orthotropic import cyl_orthotropic
from .biaxial import biaxial
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
        ['user_defined_function', 'anisotropic', 'principal_axes_values',
         'orthotropic', 'cyl_orthotropic', 'biaxial', 'expression',
         'polynomial', 'piecewise_polynomial', 'piecewise_linear', 'value',
         'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermal_conductivity.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of thermal_conductivity.
    """
    principal_axes_values: principal_axes_values = principal_axes_values
    """
    principal_axes_values child of thermal_conductivity.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of thermal_conductivity.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of thermal_conductivity.
    """
    biaxial: biaxial = biaxial
    """
    biaxial child of thermal_conductivity.
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
