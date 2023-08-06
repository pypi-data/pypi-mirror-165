#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .single_precision_coordinates import single_precision_coordinates
from .binary_legacy_files import binary_legacy_files
from .cff_files import cff_files
from .async_optimize import async_optimize
from .write_pdat import write_pdat
from .confirm_overwrite import confirm_overwrite
from .export import export
from .import_ import import_
from .auto_save import auto_save
from .define_macro import define_macro
from .read import read
from .replace_mesh import replace_mesh
from .write import write
from .parametric_project import parametric_project
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    child_names = \
        ['single_precision_coordinates', 'binary_legacy_files', 'cff_files',
         'async_optimize', 'write_pdat', 'confirm_overwrite', 'export',
         'import_']

    single_precision_coordinates: single_precision_coordinates = single_precision_coordinates
    """
    single_precision_coordinates child of file.
    """
    binary_legacy_files: binary_legacy_files = binary_legacy_files
    """
    binary_legacy_files child of file.
    """
    cff_files: cff_files = cff_files
    """
    cff_files child of file.
    """
    async_optimize: async_optimize = async_optimize
    """
    async_optimize child of file.
    """
    write_pdat: write_pdat = write_pdat
    """
    write_pdat child of file.
    """
    confirm_overwrite: confirm_overwrite = confirm_overwrite
    """
    confirm_overwrite child of file.
    """
    export: export = export
    """
    export child of file.
    """
    import_: import_ = import_
    """
    import_ child of file.
    """
    command_names = \
        ['auto_save', 'define_macro', 'read', 'replace_mesh', 'write',
         'parametric_project']

    auto_save: auto_save = auto_save
    """
    auto_save command of file.
    """
    define_macro: define_macro = define_macro
    """
    define_macro command of file.
    """
    read: read = read
    """
    read command of file.
    """
    replace_mesh: replace_mesh = replace_mesh
    """
    replace_mesh command of file.
    """
    write: write = write
    """
    write command of file.
    """
    parametric_project: parametric_project = parametric_project
    """
    parametric_project command of file.
    """
