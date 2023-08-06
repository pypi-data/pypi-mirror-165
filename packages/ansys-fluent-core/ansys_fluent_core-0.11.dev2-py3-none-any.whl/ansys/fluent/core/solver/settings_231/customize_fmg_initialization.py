#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .multi_level_grid import multi_level_grid
from .residual_reduction_level import residual_reduction_level
from .number_of_cycles import number_of_cycles
class customize_fmg_initialization(Command):
    """
    'customize_fmg_initialization' command.
    
    Parameters
    ----------
        multi_level_grid : int
            'multi_level_grid' child.
        residual_reduction_level : typing.List[real]
            'residual_reduction_level' child.
        number_of_cycles : typing.List[real]
            'number_of_cycles' child.
    
    """

    fluent_name = "customize-fmg-initialization"

    argument_names = \
        ['multi_level_grid', 'residual_reduction_level', 'number_of_cycles']

    multi_level_grid: multi_level_grid = multi_level_grid
    """
    multi_level_grid argument of customize_fmg_initialization.
    """
    residual_reduction_level: residual_reduction_level = residual_reduction_level
    """
    residual_reduction_level argument of customize_fmg_initialization.
    """
    number_of_cycles: number_of_cycles = number_of_cycles
    """
    number_of_cycles argument of customize_fmg_initialization.
    """
