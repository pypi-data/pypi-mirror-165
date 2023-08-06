#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method import method
from .time_period import time_period
from .time_steps import time_steps
class unsteady_sampling_setup(Command):
    """
    'unsteady_sampling_setup' command.
    
    Parameters
    ----------
        method : int
            'method' child.
        time_period : real
            'time_period' child.
        time_steps : int
            'time_steps' child.
    
    """

    fluent_name = "unsteady-sampling-setup"

    argument_names = \
        ['method', 'time_period', 'time_steps']

    method: method = method
    """
    method argument of unsteady_sampling_setup.
    """
    time_period: time_period = time_period
    """
    time_period argument of unsteady_sampling_setup.
    """
    time_steps: time_steps = time_steps
    """
    time_steps argument of unsteady_sampling_setup.
    """
