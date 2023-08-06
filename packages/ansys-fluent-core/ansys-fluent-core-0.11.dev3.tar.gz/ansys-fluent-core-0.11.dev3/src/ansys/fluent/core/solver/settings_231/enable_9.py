#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_mda_cht import enable_mda_cht
class enable(Command):
    """
    Enable/disable loosely coupled conjugate heat transfer.
    
    Parameters
    ----------
        enable_mda_cht : bool
            'enable_mda_cht' child.
    
    """

    fluent_name = "enable?"

    argument_names = \
        ['enable_mda_cht']

    enable_mda_cht: enable_mda_cht = enable_mda_cht
    """
    enable_mda_cht argument of enable.
    """
