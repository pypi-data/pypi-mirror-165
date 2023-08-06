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
class velocity_accom_coefficient(Group):
    """
    'velocity_accom_coefficient' child.
    """

    fluent_name = "velocity-accom-coefficient"

    child_names = \
        ['value', 'option', 'var_class']

    value: value = value
    """
    value child of velocity_accom_coefficient.
    """
    option: option = option
    """
    option child of velocity_accom_coefficient.
    """
    var_class: var_class = var_class
    """
    var_class child of velocity_accom_coefficient.
    """
