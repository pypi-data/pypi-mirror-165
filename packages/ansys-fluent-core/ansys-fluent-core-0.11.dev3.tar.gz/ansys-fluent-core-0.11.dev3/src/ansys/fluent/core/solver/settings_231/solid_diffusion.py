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
class solid_diffusion(Group):
    """
    'solid_diffusion' child.
    """

    fluent_name = "solid-diffusion"

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
    option child of solid_diffusion.
    """
    value: value = value
    """
    value child of solid_diffusion.
    """
    expression: expression = expression
    """
    expression child of solid_diffusion.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of solid_diffusion.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of solid_diffusion.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of solid_diffusion.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of solid_diffusion.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of solid_diffusion.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of solid_diffusion.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of solid_diffusion.
    """
    combustion_mixture: combustion_mixture = combustion_mixture
    """
    combustion_mixture child of solid_diffusion.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of solid_diffusion.
    """
    biaxial: biaxial = biaxial
    """
    biaxial child of solid_diffusion.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of solid_diffusion.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of solid_diffusion.
    """
    principal_axes_values: principal_axes_values = principal_axes_values
    """
    principal_axes_values child of solid_diffusion.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of solid_diffusion.
    """
    power_law: power_law = power_law
    """
    power_law child of solid_diffusion.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of solid_diffusion.
    """
    blottner_curve_fit: blottner_curve_fit = blottner_curve_fit
    """
    blottner_curve_fit child of solid_diffusion.
    """
    vibrational_modes: vibrational_modes = vibrational_modes
    """
    vibrational_modes child of solid_diffusion.
    """
    non_newtonian_power_law: non_newtonian_power_law = non_newtonian_power_law
    """
    non_newtonian_power_law child of solid_diffusion.
    """
    carreau: carreau = carreau
    """
    carreau child of solid_diffusion.
    """
    herschel_bulkley: herschel_bulkley = herschel_bulkley
    """
    herschel_bulkley child of solid_diffusion.
    """
    cross: cross = cross
    """
    cross child of solid_diffusion.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited = kinetics_diffusion_limited
    """
    kinetics_diffusion_limited child of solid_diffusion.
    """
    intrinsic_model: intrinsic_model = intrinsic_model
    """
    intrinsic_model child of solid_diffusion.
    """
    cbk: cbk = cbk
    """
    cbk child of solid_diffusion.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of solid_diffusion.
    """
    secondary_rate: secondary_rate = secondary_rate
    """
    secondary_rate child of solid_diffusion.
    """
    film_averaged: film_averaged = film_averaged
    """
    film_averaged child of solid_diffusion.
    """
    diffusion_controlled: diffusion_controlled = diffusion_controlled
    """
    diffusion_controlled child of solid_diffusion.
    """
    convection_diffusion_controlled: convection_diffusion_controlled = convection_diffusion_controlled
    """
    convection_diffusion_controlled child of solid_diffusion.
    """
    lewis_number: lewis_number = lewis_number
    """
    lewis_number child of solid_diffusion.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of solid_diffusion.
    """
    delta_eddington: delta_eddington = delta_eddington
    """
    delta_eddington child of solid_diffusion.
    """
    two_competing_rates: two_competing_rates = two_competing_rates
    """
    two_competing_rates child of solid_diffusion.
    """
    cpd_model: cpd_model = cpd_model
    """
    cpd_model child of solid_diffusion.
    """
    multiple_surface_reactions: multiple_surface_reactions = multiple_surface_reactions
    """
    multiple_surface_reactions child of solid_diffusion.
    """
    orthotropic_structure_ym: orthotropic_structure_ym = orthotropic_structure_ym
    """
    orthotropic_structure_ym child of solid_diffusion.
    """
    orthotropic_structure_nu: orthotropic_structure_nu = orthotropic_structure_nu
    """
    orthotropic_structure_nu child of solid_diffusion.
    """
    orthotropic_structure_te: orthotropic_structure_te = orthotropic_structure_te
    """
    orthotropic_structure_te child of solid_diffusion.
    """
    var_class: var_class = var_class
    """
    var_class child of solid_diffusion.
    """
