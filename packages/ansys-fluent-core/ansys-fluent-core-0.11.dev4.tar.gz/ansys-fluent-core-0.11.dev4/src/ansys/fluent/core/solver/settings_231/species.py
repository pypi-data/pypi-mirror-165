#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_8 import option
from .var_class import var_class
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['option', 'var_class']

    option: option = option
    """
    option child of species.
    """
    var_class: var_class = var_class
    """
    var_class child of species.
    """
