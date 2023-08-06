#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .multiple_surface_reactions import multiple_surface_reactions
from .intrinsic_model import intrinsic_model
from .kinetics_diffusion_limited import kinetics_diffusion_limited
from .cbk import cbk
from .option_8 import option
from .var_class import var_class
class combustion_model(Group):
    """
    'combustion_model' child.
    """

    fluent_name = "combustion-model"

    child_names = \
        ['multiple_surface_reactions', 'intrinsic_model',
         'kinetics_diffusion_limited', 'cbk', 'option', 'var_class']

    multiple_surface_reactions: multiple_surface_reactions = multiple_surface_reactions
    """
    multiple_surface_reactions child of combustion_model.
    """
    intrinsic_model: intrinsic_model = intrinsic_model
    """
    intrinsic_model child of combustion_model.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited = kinetics_diffusion_limited
    """
    kinetics_diffusion_limited child of combustion_model.
    """
    cbk: cbk = cbk
    """
    cbk child of combustion_model.
    """
    option: option = option
    """
    option child of combustion_model.
    """
    var_class: var_class = var_class
    """
    var_class child of combustion_model.
    """
