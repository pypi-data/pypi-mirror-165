#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_function import user_defined_function
from .mass_diffusivity import mass_diffusivity
from .lewis_number import lewis_number
from .option_8 import option
from .var_class import var_class
class mass_diffusivity(Group):
    """
    'mass_diffusivity' child.
    """

    fluent_name = "mass-diffusivity"

    child_names = \
        ['user_defined_function', 'mass_diffusivity', 'lewis_number',
         'option', 'var_class']

    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of mass_diffusivity.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of mass_diffusivity.
    """
    lewis_number: lewis_number = lewis_number
    """
    lewis_number child of mass_diffusivity.
    """
    option: option = option
    """
    option child of mass_diffusivity.
    """
    var_class: var_class = var_class
    """
    var_class child of mass_diffusivity.
    """
