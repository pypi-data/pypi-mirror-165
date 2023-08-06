#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .b import b
from .temperature_exponent import temperature_exponent
from .reference_viscosity import reference_viscosity
from .reference_temperature import reference_temperature
class power_law(Group):
    """
    'power_law' child.
    """

    fluent_name = "power-law"

    child_names = \
        ['option', 'b', 'temperature_exponent', 'reference_viscosity',
         'reference_temperature']

    option: option = option
    """
    option child of power_law.
    """
    b: b = b
    """
    b child of power_law.
    """
    temperature_exponent: temperature_exponent = temperature_exponent
    """
    temperature_exponent child of power_law.
    """
    reference_viscosity: reference_viscosity = reference_viscosity
    """
    reference_viscosity child of power_law.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of power_law.
    """
