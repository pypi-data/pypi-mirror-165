#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .value import value
from .secondary_rate import secondary_rate
from .single_rate import single_rate
from .option_8 import option
from .var_class import var_class
class thermolysis_model(Group):
    """
    'thermolysis_model' child.
    """

    fluent_name = "thermolysis-model"

    child_names = \
        ['value', 'secondary_rate', 'single_rate', 'option', 'var_class']

    value: value = value
    """
    value child of thermolysis_model.
    """
    secondary_rate: secondary_rate = secondary_rate
    """
    secondary_rate child of thermolysis_model.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of thermolysis_model.
    """
    option: option = option
    """
    option child of thermolysis_model.
    """
    var_class: var_class = var_class
    """
    var_class child of thermolysis_model.
    """
