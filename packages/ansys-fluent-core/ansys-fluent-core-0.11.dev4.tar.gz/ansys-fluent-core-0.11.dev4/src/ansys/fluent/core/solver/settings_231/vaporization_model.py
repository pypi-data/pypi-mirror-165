#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .convection_diffusion_controlled import convection_diffusion_controlled
from .diffusion_controlled import diffusion_controlled
from .option_8 import option
from .var_class import var_class
class vaporization_model(Group):
    """
    'vaporization_model' child.
    """

    fluent_name = "vaporization-model"

    child_names = \
        ['convection_diffusion_controlled', 'diffusion_controlled', 'option',
         'var_class']

    convection_diffusion_controlled: convection_diffusion_controlled = convection_diffusion_controlled
    """
    convection_diffusion_controlled child of vaporization_model.
    """
    diffusion_controlled: diffusion_controlled = diffusion_controlled
    """
    diffusion_controlled child of vaporization_model.
    """
    option: option = option
    """
    option child of vaporization_model.
    """
    var_class: var_class = var_class
    """
    var_class child of vaporization_model.
    """
