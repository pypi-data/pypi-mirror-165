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
class premix_laminar_thickness(Group):
    """
    'premix_laminar_thickness' child.
    """

    fluent_name = "premix-laminar-thickness"

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
    option child of premix_laminar_thickness.
    """
    value: value = value
    """
    value child of premix_laminar_thickness.
    """
    expression: expression = expression
    """
    expression child of premix_laminar_thickness.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_laminar_thickness.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of premix_laminar_thickness.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of premix_laminar_thickness.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of premix_laminar_thickness.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of premix_laminar_thickness.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of premix_laminar_thickness.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of premix_laminar_thickness.
    """
    combustion_mixture: combustion_mixture = combustion_mixture
    """
    combustion_mixture child of premix_laminar_thickness.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of premix_laminar_thickness.
    """
    biaxial: biaxial = biaxial
    """
    biaxial child of premix_laminar_thickness.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of premix_laminar_thickness.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of premix_laminar_thickness.
    """
    principal_axes_values: principal_axes_values = principal_axes_values
    """
    principal_axes_values child of premix_laminar_thickness.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of premix_laminar_thickness.
    """
    power_law: power_law = power_law
    """
    power_law child of premix_laminar_thickness.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of premix_laminar_thickness.
    """
    blottner_curve_fit: blottner_curve_fit = blottner_curve_fit
    """
    blottner_curve_fit child of premix_laminar_thickness.
    """
    vibrational_modes: vibrational_modes = vibrational_modes
    """
    vibrational_modes child of premix_laminar_thickness.
    """
    non_newtonian_power_law: non_newtonian_power_law = non_newtonian_power_law
    """
    non_newtonian_power_law child of premix_laminar_thickness.
    """
    carreau: carreau = carreau
    """
    carreau child of premix_laminar_thickness.
    """
    herschel_bulkley: herschel_bulkley = herschel_bulkley
    """
    herschel_bulkley child of premix_laminar_thickness.
    """
    cross: cross = cross
    """
    cross child of premix_laminar_thickness.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited = kinetics_diffusion_limited
    """
    kinetics_diffusion_limited child of premix_laminar_thickness.
    """
    intrinsic_model: intrinsic_model = intrinsic_model
    """
    intrinsic_model child of premix_laminar_thickness.
    """
    cbk: cbk = cbk
    """
    cbk child of premix_laminar_thickness.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of premix_laminar_thickness.
    """
    secondary_rate: secondary_rate = secondary_rate
    """
    secondary_rate child of premix_laminar_thickness.
    """
    film_averaged: film_averaged = film_averaged
    """
    film_averaged child of premix_laminar_thickness.
    """
    diffusion_controlled: diffusion_controlled = diffusion_controlled
    """
    diffusion_controlled child of premix_laminar_thickness.
    """
    convection_diffusion_controlled: convection_diffusion_controlled = convection_diffusion_controlled
    """
    convection_diffusion_controlled child of premix_laminar_thickness.
    """
    lewis_number: lewis_number = lewis_number
    """
    lewis_number child of premix_laminar_thickness.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of premix_laminar_thickness.
    """
    delta_eddington: delta_eddington = delta_eddington
    """
    delta_eddington child of premix_laminar_thickness.
    """
    two_competing_rates: two_competing_rates = two_competing_rates
    """
    two_competing_rates child of premix_laminar_thickness.
    """
    cpd_model: cpd_model = cpd_model
    """
    cpd_model child of premix_laminar_thickness.
    """
    multiple_surface_reactions: multiple_surface_reactions = multiple_surface_reactions
    """
    multiple_surface_reactions child of premix_laminar_thickness.
    """
    orthotropic_structure_ym: orthotropic_structure_ym = orthotropic_structure_ym
    """
    orthotropic_structure_ym child of premix_laminar_thickness.
    """
    orthotropic_structure_nu: orthotropic_structure_nu = orthotropic_structure_nu
    """
    orthotropic_structure_nu child of premix_laminar_thickness.
    """
    orthotropic_structure_te: orthotropic_structure_te = orthotropic_structure_te
    """
    orthotropic_structure_te child of premix_laminar_thickness.
    """
    var_class: var_class = var_class
    """
    var_class child of premix_laminar_thickness.
    """
