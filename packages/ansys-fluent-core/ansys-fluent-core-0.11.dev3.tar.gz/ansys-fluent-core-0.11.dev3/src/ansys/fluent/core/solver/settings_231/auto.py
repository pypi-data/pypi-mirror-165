#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .across_zones import across_zones
from .method_1 import method
from .load_vector import load_vector
from .pre_test import pre_test
from .auto_partition_method import auto_partition_method
from .use_case_file_method import use_case_file_method
class auto(Group):
    """
    Enter the menu to set auto partition parameters.
    """

    fluent_name = "auto"

    child_names = \
        ['across_zones', 'method', 'load_vector', 'pre_test']

    across_zones: across_zones = across_zones
    """
    across_zones child of auto.
    """
    method: method = method
    """
    method child of auto.
    """
    load_vector: load_vector = load_vector
    """
    load_vector child of auto.
    """
    pre_test: pre_test = pre_test
    """
    pre_test child of auto.
    """
    command_names = \
        ['auto_partition_method', 'use_case_file_method']

    auto_partition_method: auto_partition_method = auto_partition_method
    """
    auto_partition_method command of auto.
    """
    use_case_file_method: use_case_file_method = use_case_file_method
    """
    use_case_file_method command of auto.
    """
