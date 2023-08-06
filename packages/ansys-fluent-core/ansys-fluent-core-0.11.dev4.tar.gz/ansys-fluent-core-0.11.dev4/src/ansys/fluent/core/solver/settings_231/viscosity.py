#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .real_gas_nist import real_gas_nist
from .rgp_table import rgp_table
from .user_defined_function import user_defined_function
from .non_newtonian_power_law import non_newtonian_power_law
from .carreau import carreau
from .herschel_bulkley import herschel_bulkley
from .cross import cross
from .sutherland import sutherland
from .blottner_curve_fit import blottner_curve_fit
from .power_law import power_law
from .expression import expression
from .polynomial import polynomial
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .value import value
from .option_8 import option
from .var_class import var_class
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['real_gas_nist', 'rgp_table', 'user_defined_function',
         'non_newtonian_power_law', 'carreau', 'herschel_bulkley', 'cross',
         'sutherland', 'blottner_curve_fit', 'power_law', 'expression',
         'polynomial', 'piecewise_polynomial', 'piecewise_linear', 'value',
         'option', 'var_class']

    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of viscosity.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of viscosity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of viscosity.
    """
    non_newtonian_power_law: non_newtonian_power_law = non_newtonian_power_law
    """
    non_newtonian_power_law child of viscosity.
    """
    carreau: carreau = carreau
    """
    carreau child of viscosity.
    """
    herschel_bulkley: herschel_bulkley = herschel_bulkley
    """
    herschel_bulkley child of viscosity.
    """
    cross: cross = cross
    """
    cross child of viscosity.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of viscosity.
    """
    blottner_curve_fit: blottner_curve_fit = blottner_curve_fit
    """
    blottner_curve_fit child of viscosity.
    """
    power_law: power_law = power_law
    """
    power_law child of viscosity.
    """
    expression: expression = expression
    """
    expression child of viscosity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of viscosity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of viscosity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of viscosity.
    """
    value: value = value
    """
    value child of viscosity.
    """
    option: option = option
    """
    option child of viscosity.
    """
    var_class: var_class = var_class
    """
    var_class child of viscosity.
    """
