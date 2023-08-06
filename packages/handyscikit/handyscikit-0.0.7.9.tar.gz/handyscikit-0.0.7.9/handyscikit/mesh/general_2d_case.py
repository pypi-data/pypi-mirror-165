from handyscikit.mesh.core.gmsh_encapsulation import GmshEncapsulation
from handyscikit.mesh.core.mesh_2d import Mesh2D
from handyscikit.mesh.core.mesh_base import meshing_timer
import gmsh


class General2DCase(Mesh2D, GmshEncapsulation):
    def __init__(self):
        Mesh2D.__init__(self)

        self._dim = 2
        self._node_per_face = 2

        self._gmsh_element_type = 2  # 2 means triangle.
        self._face_per_cell = 3
        self._node_per_cell = 3

    @meshing_timer
    def generate_unstructured(self, show_mesh=False):

        gmsh.model.mesh.generate(2)
        if self._gmsh_element_type == 3: gmsh.model.mesh.recombine()
        if show_mesh: gmsh.fltk.run()

        self._generate_topology()