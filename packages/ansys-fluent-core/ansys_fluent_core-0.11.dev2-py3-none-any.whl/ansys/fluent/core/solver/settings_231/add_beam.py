#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .beam_name import beam_name
from .face_zone_id import face_zone_id
from .beam_length import beam_length
from .ray_npnts import ray_npnts
from .x_beam_vector import x_beam_vector
from .y_beam_vector import y_beam_vector
from .z_beam_vector import z_beam_vector
class add_beam(Command):
    """
    Add optical beam grid.
    
    Parameters
    ----------
        beam_name : str
            'beam_name' child.
        face_zone_id : int
            'face_zone_id' child.
        beam_length : real
            'beam_length' child.
        ray_npnts : int
            'ray_npnts' child.
        x_beam_vector : real
            'x_beam_vector' child.
        y_beam_vector : real
            'y_beam_vector' child.
        z_beam_vector : real
            'z_beam_vector' child.
    
    """

    fluent_name = "add-beam"

    argument_names = \
        ['beam_name', 'face_zone_id', 'beam_length', 'ray_npnts',
         'x_beam_vector', 'y_beam_vector', 'z_beam_vector']

    beam_name: beam_name = beam_name
    """
    beam_name argument of add_beam.
    """
    face_zone_id: face_zone_id = face_zone_id
    """
    face_zone_id argument of add_beam.
    """
    beam_length: beam_length = beam_length
    """
    beam_length argument of add_beam.
    """
    ray_npnts: ray_npnts = ray_npnts
    """
    ray_npnts argument of add_beam.
    """
    x_beam_vector: x_beam_vector = x_beam_vector
    """
    x_beam_vector argument of add_beam.
    """
    y_beam_vector: y_beam_vector = y_beam_vector
    """
    y_beam_vector argument of add_beam.
    """
    z_beam_vector: z_beam_vector = z_beam_vector
    """
    z_beam_vector argument of add_beam.
    """
