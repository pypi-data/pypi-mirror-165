#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_optics import enable_optics
class enable(Command):
    """
    Enable/disable aero-optical model.
    
    Parameters
    ----------
        enable_optics : bool
            'enable_optics' child.
    
    """

    fluent_name = "enable?"

    argument_names = \
        ['enable_optics']

    enable_optics: enable_optics = enable_optics
    """
    enable_optics argument of enable.
    """
