from .core.mesh_2d import Mesh2D
from .core.mesh_base import meshing_timer
import gmsh


class CircleCase(Mesh2D):
    def __init__(self, size):
        Mesh2D.__init__(self)

        # gmsh.model.occ.addDisk(xc, yc, zc, rx, ry, tag=-1, zAxis=[], xAxis=[])
        gmsh.model.occ.add_disk(0, 0, 0, size, size)
        gmsh.model.occ.synchronize()

        self._dim = 2
        self._node_per_face = 2
        self._size = size

    @meshing_timer
    def generate_unstructured(self, size_list=None, show_mesh=False):
        self._gmsh_element_type = 2  # 2 means triangle.
        self._face_per_cell = 3
        self._node_per_cell = 3

        if size_list is not None:
            gmsh.model.mesh.set_size([(0, 1)], size_list[0])
        gmsh.model.mesh.generate(2)
        if show_mesh:
            gmsh.fltk.run()
        self._generate_topology()

    @property
    def boundary(self):
        return 1

    @property
    def size(self):
        return self._size
