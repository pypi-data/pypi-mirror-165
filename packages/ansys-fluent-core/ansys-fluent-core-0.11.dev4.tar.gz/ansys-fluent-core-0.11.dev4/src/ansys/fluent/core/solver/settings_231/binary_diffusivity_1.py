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
from .film_averaged import film_averaged
from .value import value
from .option_8 import option
from .var_class import var_class
class binary_diffusivity(Group):
    """
    'binary_diffusivity' child.
    """

    fluent_name = "binary-diffusivity"

    child_names = \
        ['user_defined_function', 'polynomial', 'piecewise_polynomial',
         'piecewise_linear', 'film_averaged', 'value', 'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of binary_diffusivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of binary_diffusivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of binary_diffusivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of binary_diffusivity.
    """
    film_averaged: film_averaged = film_averaged
    """
    film_averaged child of binary_diffusivity.
    """
    value: value = value
    """
    value child of binary_diffusivity.
    """
    option: option = option
    """
    option child of binary_diffusivity.
    """
    var_class: var_class = var_class
    """
    var_class child of binary_diffusivity.
    """
