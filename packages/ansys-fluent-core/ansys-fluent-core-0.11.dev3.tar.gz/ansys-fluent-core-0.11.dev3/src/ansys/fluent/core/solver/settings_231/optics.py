#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_1 import set
from .add_beam import add_beam
from .enable_3 import enable
class optics(Group):
    """
    Enter the optics model menu.
    """

    fluent_name = "optics"

    child_names = \
        ['set']

    set: set = set
    """
    set child of optics.
    """
    command_names = \
        ['add_beam', 'enable']

    add_beam: add_beam = add_beam
    """
    add_beam command of optics.
    """
    enable: enable = enable
    """
    enable command of optics.
    """
