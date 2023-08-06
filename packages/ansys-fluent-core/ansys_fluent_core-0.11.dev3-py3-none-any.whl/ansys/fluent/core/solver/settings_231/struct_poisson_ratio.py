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
class struct_poisson_ratio(Group):
    """
    'struct_poisson_ratio' child.
    """

    fluent_name = "struct-poisson-ratio"

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
    option child of struct_poisson_ratio.
    """
    value: value = value
    """
    value child of struct_poisson_ratio.
    """
    expression: expression = expression
    """
    expression child of struct_poisson_ratio.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of struct_poisson_ratio.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of struct_poisson_ratio.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of struct_poisson_ratio.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of struct_poisson_ratio.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of struct_poisson_ratio.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of struct_poisson_ratio.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of struct_poisson_ratio.
    """
    combustion_mixture: combustion_mixture = combustion_mixture
    """
    combustion_mixture child of struct_poisson_ratio.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of struct_poisson_ratio.
    """
    biaxial: biaxial = biaxial
    """
    biaxial child of struct_poisson_ratio.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of struct_poisson_ratio.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of struct_poisson_ratio.
    """
    principal_axes_values: principal_axes_values = principal_axes_values
    """
    principal_axes_values child of struct_poisson_ratio.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of struct_poisson_ratio.
    """
    power_law: power_law = power_law
    """
    power_law child of struct_poisson_ratio.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of struct_poisson_ratio.
    """
    blottner_curve_fit: blottner_curve_fit = blottner_curve_fit
    """
    blottner_curve_fit child of struct_poisson_ratio.
    """
    vibrational_modes: vibrational_modes = vibrational_modes
    """
    vibrational_modes child of struct_poisson_ratio.
    """
    non_newtonian_power_law: non_newtonian_power_law = non_newtonian_power_law
    """
    non_newtonian_power_law child of struct_poisson_ratio.
    """
    carreau: carreau = carreau
    """
    carreau child of struct_poisson_ratio.
    """
    herschel_bulkley: herschel_bulkley = herschel_bulkley
    """
    herschel_bulkley child of struct_poisson_ratio.
    """
    cross: cross = cross
    """
    cross child of struct_poisson_ratio.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited = kinetics_diffusion_limited
    """
    kinetics_diffusion_limited child of struct_poisson_ratio.
    """
    intrinsic_model: intrinsic_model = intrinsic_model
    """
    intrinsic_model child of struct_poisson_ratio.
    """
    cbk: cbk = cbk
    """
    cbk child of struct_poisson_ratio.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of struct_poisson_ratio.
    """
    secondary_rate: secondary_rate = secondary_rate
    """
    secondary_rate child of struct_poisson_ratio.
    """
    film_averaged: film_averaged = film_averaged
    """
    film_averaged child of struct_poisson_ratio.
    """
    diffusion_controlled: diffusion_controlled = diffusion_controlled
    """
    diffusion_controlled child of struct_poisson_ratio.
    """
    convection_diffusion_controlled: convection_diffusion_controlled = convection_diffusion_controlled
    """
    convection_diffusion_controlled child of struct_poisson_ratio.
    """
    lewis_number: lewis_number = lewis_number
    """
    lewis_number child of struct_poisson_ratio.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of struct_poisson_ratio.
    """
    delta_eddington: delta_eddington = delta_eddington
    """
    delta_eddington child of struct_poisson_ratio.
    """
    two_competing_rates: two_competing_rates = two_competing_rates
    """
    two_competing_rates child of struct_poisson_ratio.
    """
    cpd_model: cpd_model = cpd_model
    """
    cpd_model child of struct_poisson_ratio.
    """
    multiple_surface_reactions: multiple_surface_reactions = multiple_surface_reactions
    """
    multiple_surface_reactions child of struct_poisson_ratio.
    """
    orthotropic_structure_ym: orthotropic_structure_ym = orthotropic_structure_ym
    """
    orthotropic_structure_ym child of struct_poisson_ratio.
    """
    orthotropic_structure_nu: orthotropic_structure_nu = orthotropic_structure_nu
    """
    orthotropic_structure_nu child of struct_poisson_ratio.
    """
    orthotropic_structure_te: orthotropic_structure_te = orthotropic_structure_te
    """
    orthotropic_structure_te child of struct_poisson_ratio.
    """
    var_class: var_class = var_class
    """
    var_class child of struct_poisson_ratio.
    """
