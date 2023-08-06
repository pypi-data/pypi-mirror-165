#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .mesh_2 import mesh
from .contour import contour
from .vector import vector
from .pathline import pathline
from .particle_track import particle_track
from .lic import lic
from .views import views
from .colors import colors
from .windows import windows
from .lights import lights
from .contours import contours
from .particle_tracks import particle_tracks
class graphics(Group, _ChildNamedObjectAccessorMixin):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['mesh', 'contour', 'vector', 'pathline', 'particle_track', 'lic',
         'views', 'colors', 'windows', 'lights', 'contours',
         'particle_tracks']

    mesh: mesh = mesh
    """
    mesh child of graphics.
    """
    contour: contour = contour
    """
    contour child of graphics.
    """
    vector: vector = vector
    """
    vector child of graphics.
    """
    pathline: pathline = pathline
    """
    pathline child of graphics.
    """
    particle_track: particle_track = particle_track
    """
    particle_track child of graphics.
    """
    lic: lic = lic
    """
    lic child of graphics.
    """
    views: views = views
    """
    views child of graphics.
    """
    colors: colors = colors
    """
    colors child of graphics.
    """
    windows: windows = windows
    """
    windows child of graphics.
    """
    lights: lights = lights
    """
    lights child of graphics.
    """
    contours: contours = contours
    """
    contours child of graphics.
    """
    particle_tracks: particle_tracks = particle_tracks
    """
    particle_tracks child of graphics.
    """
