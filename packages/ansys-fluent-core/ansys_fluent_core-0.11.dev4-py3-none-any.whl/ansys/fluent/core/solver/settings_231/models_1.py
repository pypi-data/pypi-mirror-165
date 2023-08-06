#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .discrete_phase import discrete_phase
from .energy import energy
from .multiphase import multiphase
from .viscous import viscous
from .optics import optics
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['discrete_phase', 'energy', 'multiphase', 'viscous', 'optics']

    discrete_phase: discrete_phase = discrete_phase
    """
    discrete_phase child of models.
    """
    energy: energy = energy
    """
    energy child of models.
    """
    multiphase: multiphase = multiphase
    """
    multiphase child of models.
    """
    viscous: viscous = viscous
    """
    viscous child of models.
    """
    optics: optics = optics
    """
    optics child of models.
    """
