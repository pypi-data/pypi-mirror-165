#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .rgp_table import rgp_table
from .value import value
from .option_8 import option
from .var_class import var_class
class molecular_weight(Group):
    """
    'molecular_weight' child.
    """

    fluent_name = "molecular-weight"

    child_names = \
        ['rgp_table', 'value', 'option', 'var_class']

    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of molecular_weight.
    """
    value: value = value
    """
    value child of molecular_weight.
    """
    option: option = option
    """
    option child of molecular_weight.
    """
    var_class: var_class = var_class
    """
    var_class child of molecular_weight.
    """
