#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axes_2 import axes
from .main import main
from .scale_3 import scale
from .text import text
from .video import video
from .xy import xy
from .logo import logo
from .ruler_1 import ruler
class windows(Group):
    """
    'windows' child.
    """

    fluent_name = "windows"

    child_names = \
        ['axes', 'main', 'scale', 'text', 'video', 'xy', 'logo', 'ruler']

    axes: axes = axes
    """
    axes child of windows.
    """
    main: main = main
    """
    main child of windows.
    """
    scale: scale = scale
    """
    scale child of windows.
    """
    text: text = text
    """
    text child of windows.
    """
    video: video = video
    """
    video child of windows.
    """
    xy: xy = xy
    """
    xy child of windows.
    """
    logo: logo = logo
    """
    logo child of windows.
    """
    ruler: ruler = ruler
    """
    ruler child of windows.
    """
