#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .coupling import coupling
from .session_mode import session_mode
from .helper_session import helper_session
class set(Group):
    """
    'set' child.
    """

    fluent_name = "set"

    child_names = \
        ['coupling', 'session_mode', 'helper_session']

    coupling: coupling = coupling
    """
    coupling child of set.
    """
    session_mode: session_mode = session_mode
    """
    session_mode child of set.
    """
    helper_session: helper_session = helper_session
    """
    helper_session child of set.
    """
