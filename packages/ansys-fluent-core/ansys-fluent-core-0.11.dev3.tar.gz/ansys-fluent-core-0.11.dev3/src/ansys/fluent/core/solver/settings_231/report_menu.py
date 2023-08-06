#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .discrete_phase_1 import discrete_phase
from .fluxes import fluxes
from .flow import flow
from .modified_setting_options import modified_setting_options
from .population_balance import population_balance
from .heat_exchange import heat_exchange
from .system import system
from .mphase_summary import mphase_summary
from .print_write_histogram import print_write_histogram
from .aero_optical_distortions import aero_optical_distortions
from .forces import forces
from .particle_summary import particle_summary
from .path_line_summary import path_line_summary
from .projected_surface_area import projected_surface_area
from .summary_1 import summary
from .surface_integrals import surface_integrals
from .volume_integrals import volume_integrals
class report_menu(Group):
    """
    'report_menu' child.
    """

    fluent_name = "report-menu"

    child_names = \
        ['discrete_phase', 'fluxes', 'flow', 'modified_setting_options',
         'population_balance', 'heat_exchange', 'system', 'mphase_summary',
         'print_write_histogram']

    discrete_phase: discrete_phase = discrete_phase
    """
    discrete_phase child of report_menu.
    """
    fluxes: fluxes = fluxes
    """
    fluxes child of report_menu.
    """
    flow: flow = flow
    """
    flow child of report_menu.
    """
    modified_setting_options: modified_setting_options = modified_setting_options
    """
    modified_setting_options child of report_menu.
    """
    population_balance: population_balance = population_balance
    """
    population_balance child of report_menu.
    """
    heat_exchange: heat_exchange = heat_exchange
    """
    heat_exchange child of report_menu.
    """
    system: system = system
    """
    system child of report_menu.
    """
    mphase_summary: mphase_summary = mphase_summary
    """
    mphase_summary child of report_menu.
    """
    print_write_histogram: print_write_histogram = print_write_histogram
    """
    print_write_histogram child of report_menu.
    """
    command_names = \
        ['aero_optical_distortions', 'forces', 'particle_summary',
         'path_line_summary', 'projected_surface_area', 'summary',
         'surface_integrals', 'volume_integrals']

    aero_optical_distortions: aero_optical_distortions = aero_optical_distortions
    """
    aero_optical_distortions command of report_menu.
    """
    forces: forces = forces
    """
    forces command of report_menu.
    """
    particle_summary: particle_summary = particle_summary
    """
    particle_summary command of report_menu.
    """
    path_line_summary: path_line_summary = path_line_summary
    """
    path_line_summary command of report_menu.
    """
    projected_surface_area: projected_surface_area = projected_surface_area
    """
    projected_surface_area command of report_menu.
    """
    summary: summary = summary
    """
    summary command of report_menu.
    """
    surface_integrals: surface_integrals = surface_integrals
    """
    surface_integrals command of report_menu.
    """
    volume_integrals: volume_integrals = volume_integrals
    """
    volume_integrals command of report_menu.
    """
