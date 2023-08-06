#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .steady_iterations import steady_iterations
from .unsteady_sampling_setup import unsteady_sampling_setup
class sampling(Group):
    """
    Specify when the fluid density field is sampled.
    """

    fluent_name = "sampling"

    child_names = \
        ['steady_iterations']

    steady_iterations: steady_iterations = steady_iterations
    """
    steady_iterations child of sampling.
    """
    command_names = \
        ['unsteady_sampling_setup']

    unsteady_sampling_setup: unsteady_sampling_setup = unsteady_sampling_setup
    """
    unsteady_sampling_setup command of sampling.
    """
