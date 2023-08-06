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
class speed_of_sound(Group):
    """
    'speed_of_sound' child.
    """

    fluent_name = "speed-of-sound"

    child_names = \
        ['user_defined_function', 'expression', 'polynomial',
         'piecewise_polynomial', 'piecewise_linear', 'value', 'option',
         'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of speed_of_sound.
    """
    expression: expression = expression
    """
    expression child of speed_of_sound.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of speed_of_sound.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of speed_of_sound.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of speed_of_sound.
    """
    value: value = value
    """
    value child of speed_of_sound.
    """
    option: option = option
    """
    option child of speed_of_sound.
    """
    var_class: var_class = var_class
    """
    var_class child of speed_of_sound.
    """
