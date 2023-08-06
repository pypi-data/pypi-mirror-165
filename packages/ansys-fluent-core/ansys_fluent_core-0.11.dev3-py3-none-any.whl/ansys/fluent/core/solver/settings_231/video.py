#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .background_1 import background
from .color_filter import color_filter
from .foreground_1 import foreground
from .on import on
class video(Group):
    """
    Enter the video window options menu.
    """

    fluent_name = "video"

    child_names = \
        ['background', 'color_filter', 'foreground', 'on']

    background: background = background
    """
    background child of video.
    """
    color_filter: color_filter = color_filter
    """
    color_filter child of video.
    """
    foreground: foreground = foreground
    """
    foreground child of video.
    """
    on: on = on
    """
    on child of video.
    """
