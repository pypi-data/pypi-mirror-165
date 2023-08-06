#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .cpd_model import cpd_model
from .two_competing_rates import two_competing_rates
from .single_rate import single_rate
from .value import value
from .option_8 import option
from .var_class import var_class
class devolatilization_model(Group):
    """
    'devolatilization_model' child.
    """

    fluent_name = "devolatilization-model"

    child_names = \
        ['cpd_model', 'two_competing_rates', 'single_rate', 'value', 'option',
         'var_class']

    cpd_model: cpd_model = cpd_model
    """
    cpd_model child of devolatilization_model.
    """
    two_competing_rates: two_competing_rates = two_competing_rates
    """
    two_competing_rates child of devolatilization_model.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of devolatilization_model.
    """
    value: value = value
    """
    value child of devolatilization_model.
    """
    option: option = option
    """
    option child of devolatilization_model.
    """
    var_class: var_class = var_class
    """
    var_class child of devolatilization_model.
    """
