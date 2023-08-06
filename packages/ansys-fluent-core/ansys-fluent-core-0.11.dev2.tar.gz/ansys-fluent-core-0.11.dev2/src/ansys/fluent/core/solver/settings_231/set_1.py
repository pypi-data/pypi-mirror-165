#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .index_of_refraction import index_of_refraction
from .running_average import running_average
from .sampling import sampling
class set(Group):
    """
    Enter the set menu for aero-optical model.
    """

    fluent_name = "set"

    child_names = \
        ['index_of_refraction', 'running_average', 'sampling']

    index_of_refraction: index_of_refraction = index_of_refraction
    """
    index_of_refraction child of set.
    """
    running_average: running_average = running_average
    """
    running_average child of set.
    """
    sampling: sampling = sampling
    """
    sampling child of set.
    """
