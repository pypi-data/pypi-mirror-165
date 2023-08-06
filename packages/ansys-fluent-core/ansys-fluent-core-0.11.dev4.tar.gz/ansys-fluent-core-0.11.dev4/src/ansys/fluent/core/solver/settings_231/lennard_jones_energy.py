#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .value import value
from .option_8 import option
from .var_class import var_class
class lennard_jones_energy(Group):
    """
    'lennard_jones_energy' child.
    """

    fluent_name = "lennard-jones-energy"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of lennard_jones_energy.
    """
    option: option = option
    """
    option child of lennard_jones_energy.
    """
    var_class: var_class = var_class
    """
    var_class child of lennard_jones_energy.
    """
