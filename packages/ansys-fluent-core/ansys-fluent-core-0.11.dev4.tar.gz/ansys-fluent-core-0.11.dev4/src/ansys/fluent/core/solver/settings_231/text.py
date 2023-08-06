#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .border_3 import border
from .bottom_3 import bottom
from .clear_3 import clear
from .left_2 import left
from .right_4 import right
from .top_2 import top
from .visible_4 import visible
class text(Group):
    """
    Enter the text window options menu.
    """

    fluent_name = "text"

    child_names = \
        ['border', 'bottom', 'clear', 'left', 'right', 'top', 'visible']

    border: border = border
    """
    border child of text.
    """
    bottom: bottom = bottom
    """
    bottom child of text.
    """
    clear: clear = clear
    """
    clear child of text.
    """
    left: left = left
    """
    left child of text.
    """
    right: right = right
    """
    right child of text.
    """
    top: top = top
    """
    top child of text.
    """
    visible: visible = visible
    """
    visible child of text.
    """
