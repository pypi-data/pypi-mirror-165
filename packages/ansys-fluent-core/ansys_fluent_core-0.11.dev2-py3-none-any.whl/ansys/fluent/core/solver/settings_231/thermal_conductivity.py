#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_8 import option
from .value import value
from .expression import expression
from .user_defined_function import user_defined_function
from .piecewise_polynomial import piecewise_polynomial
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .polynomial import polynomial
from .real_gas_nist import real_gas_nist
from .rgp_table import rgp_table
from .combustion_mixture import combustion_mixture
from .anisotropic import anisotropic
from .biaxial import biaxial
from .cyl_orthotropic import cyl_orthotropic
from .orthotropic import orthotropic
from .principal_axes_values import principal_axes_values
from .sutherland import sutherland
from .power_law import power_law
from .compressible_liquid import compressible_liquid
from .blottner_curve_fit import blottner_curve_fit
from .vibrational_modes import vibrational_modes
from .non_newtonian_power_law import non_newtonian_power_law
from .carreau import carreau
from .herschel_bulkley import herschel_bulkley
from .cross import cross
from .kinetics_diffusion_limited import kinetics_diffusion_limited
from .intrinsic_model import intrinsic_model
from .cbk import cbk
from .single_rate import single_rate
from .secondary_rate import secondary_rate
from .film_averaged import film_averaged
from .diffusion_controlled import diffusion_controlled
from .convection_diffusion_controlled import convection_diffusion_controlled
from .lewis_number import lewis_number
from .mass_diffusivity import mass_diffusivity
from .delta_eddington import delta_eddington
from .two_competing_rates import two_competing_rates
from .cpd_model import cpd_model
from .multiple_surface_reactions import multiple_surface_reactions
from .orthotropic_structure_ym import orthotropic_structure_ym
from .orthotropic_structure_nu import orthotropic_structure_nu
from .orthotropic_structure_te import orthotropic_structure_te
from .var_class import var_class
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'expression', 'user_defined_function',
         'piecewise_polynomial', 'nasa_9_piecewise_polynomial',
         'piecewise_linear', 'polynomial', 'real_gas_nist', 'rgp_table',
         'combustion_mixture', 'anisotropic', 'biaxial', 'cyl_orthotropic',
         'orthotropic', 'principal_axes_values', 'sutherland', 'power_law',
         'compressible_liquid', 'blottner_curve_fit', 'vibrational_modes',
         'non_newtonian_power_law', 'carreau', 'herschel_bulkley', 'cross',
         'kinetics_diffusion_limited', 'intrinsic_model', 'cbk',
         'single_rate', 'secondary_rate', 'film_averaged',
         'diffusion_controlled', 'convection_diffusion_controlled',
         'lewis_number', 'mass_diffusivity', 'delta_eddington',
         'two_competing_rates', 'cpd_model', 'multiple_surface_reactions',
         'orthotropic_structure_ym', 'orthotropic_structure_nu',
         'orthotropic_structure_te', 'var_class']

    option: option = option
    """
    option child of thermal_conductivity.
    """
    value: value = value
    """
    value child of thermal_conductivity.
    """
    expression: expression = expression
    """
    expression child of thermal_conductivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermal_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermal_conductivity.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of thermal_conductivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermal_conductivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of thermal_conductivity.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of thermal_conductivity.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of thermal_conductivity.
    """
    combustion_mixture: combustion_mixture = combustion_mixture
    """
    combustion_mixture child of thermal_conductivity.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of thermal_conductivity.
    """
    biaxial: biaxial = biaxial
    """
    biaxial child of thermal_conductivity.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of thermal_conductivity.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of thermal_conductivity.
    """
    principal_axes_values: principal_axes_values = principal_axes_values
    """
    principal_axes_values child of thermal_conductivity.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of thermal_conductivity.
    """
    power_law: power_law = power_law
    """
    power_law child of thermal_conductivity.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of thermal_conductivity.
    """
    blottner_curve_fit: blottner_curve_fit = blottner_curve_fit
    """
    blottner_curve_fit child of thermal_conductivity.
    """
    vibrational_modes: vibrational_modes = vibrational_modes
    """
    vibrational_modes child of thermal_conductivity.
    """
    non_newtonian_power_law: non_newtonian_power_law = non_newtonian_power_law
    """
    non_newtonian_power_law child of thermal_conductivity.
    """
    carreau: carreau = carreau
    """
    carreau child of thermal_conductivity.
    """
    herschel_bulkley: herschel_bulkley = herschel_bulkley
    """
    herschel_bulkley child of thermal_conductivity.
    """
    cross: cross = cross
    """
    cross child of thermal_conductivity.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited = kinetics_diffusion_limited
    """
    kinetics_diffusion_limited child of thermal_conductivity.
    """
    intrinsic_model: intrinsic_model = intrinsic_model
    """
    intrinsic_model child of thermal_conductivity.
    """
    cbk: cbk = cbk
    """
    cbk child of thermal_conductivity.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of thermal_conductivity.
    """
    secondary_rate: secondary_rate = secondary_rate
    """
    secondary_rate child of thermal_conductivity.
    """
    film_averaged: film_averaged = film_averaged
    """
    film_averaged child of thermal_conductivity.
    """
    diffusion_controlled: diffusion_controlled = diffusion_controlled
    """
    diffusion_controlled child of thermal_conductivity.
    """
    convection_diffusion_controlled: convection_diffusion_controlled = convection_diffusion_controlled
    """
    convection_diffusion_controlled child of thermal_conductivity.
    """
    lewis_number: lewis_number = lewis_number
    """
    lewis_number child of thermal_conductivity.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of thermal_conductivity.
    """
    delta_eddington: delta_eddington = delta_eddington
    """
    delta_eddington child of thermal_conductivity.
    """
    two_competing_rates: two_competing_rates = two_competing_rates
    """
    two_competing_rates child of thermal_conductivity.
    """
    cpd_model: cpd_model = cpd_model
    """
    cpd_model child of thermal_conductivity.
    """
    multiple_surface_reactions: multiple_surface_reactions = multiple_surface_reactions
    """
    multiple_surface_reactions child of thermal_conductivity.
    """
    orthotropic_structure_ym: orthotropic_structure_ym = orthotropic_structure_ym
    """
    orthotropic_structure_ym child of thermal_conductivity.
    """
    orthotropic_structure_nu: orthotropic_structure_nu = orthotropic_structure_nu
    """
    orthotropic_structure_nu child of thermal_conductivity.
    """
    orthotropic_structure_te: orthotropic_structure_te = orthotropic_structure_te
    """
    orthotropic_structure_te child of thermal_conductivity.
    """
    var_class: var_class = var_class
    """
    var_class child of thermal_conductivity.
    """
