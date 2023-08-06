#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method_1 import method
class auto_partition_method(Command):
    """
    Set the method for auto partitioning the domain.
    
    Parameters
    ----------
        method : str
            'method' child.
    
    """

    fluent_name = "auto-partition-method"

    argument_names = \
        ['method']

    method: method = method
    """
    method argument of auto_partition_method.
    """
