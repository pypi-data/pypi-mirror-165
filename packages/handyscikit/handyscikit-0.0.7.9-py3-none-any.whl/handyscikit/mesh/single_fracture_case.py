from .core.mesh_2d import Mesh2D
from .core.mesh_base import meshing_timer
import gmsh


class SingleFractureCase(Mesh2D):
    def __init__(self, size, coordinate=[0, 0]):
        Mesh2D.__init__(self)

        rectangle_tag = gmsh.model.occ.add_rectangle(coordinate[0], coordinate[1], 0, size[0], size[1])

        point_1_tag = gmsh.model.occ.add_point(coordinate[0], 0.5 * size[1], 0)
        point_2_tag = gmsh.model.occ.add_point(size[0], 0.5 * size[1], 0)

        line_tag = gmsh.model.occ.add_line(point_1_tag, point_2_tag)

        gmsh.model.occ.fragment([(2, rectangle_tag)], [(1, line_tag)])
        gmsh.model.occ.synchronize()

        self._dim = 2
        self._node_per_face = 2
        self._size = size
        # self._structured_num = None
        self._mesh_size_list = [0.2 for _ in range(6)]

    def set_fracture_mesh_size(self, size):
        """
        The mesh size of point_index[0]、[3] need to refine
        """
        self._mesh_size_list[0] = size
        self._mesh_size_list[3] = size

    def set_mean_size(self, size):
        self._mesh_size_list[1] = size
        self._mesh_size_list[2] = size
        self._mesh_size_list[4] = size
        self._mesh_size_list[5] = size

    @meshing_timer
    def generate_unstructured(self, size_list=None, show_mesh=False):
        self._gmsh_element_type = 2  # 2 means triangle.
        self._face_per_cell = 3
        self._node_per_cell = 3

        if size_list is not None:
            gmsh.model.mesh.set_size([(0, 1)], size_list[0])
            gmsh.model.mesh.set_size([(0, 2)], size_list[1])
            gmsh.model.mesh.set_size([(0, 3)], size_list[2])
            gmsh.model.mesh.set_size([(0, 4)], size_list[3])
            gmsh.model.mesh.set_size([(0, 5)], size_list[4])
            gmsh.model.mesh.set_size([(0, 6)], size_list[5])
        else:
            gmsh.model.mesh.set_size([(0, 1)], self._mesh_size_list[0])
            gmsh.model.mesh.set_size([(0, 2)], self._mesh_size_list[1])
            gmsh.model.mesh.set_size([(0, 3)], self._mesh_size_list[2])
            gmsh.model.mesh.set_size([(0, 4)], self._mesh_size_list[3])
            gmsh.model.mesh.set_size([(0, 5)], self._mesh_size_list[4])
            gmsh.model.mesh.set_size([(0, 6)], self._mesh_size_list[5])
        gmsh.model.mesh.generate(2)
        if show_mesh:
            gmsh.fltk.run()

        self._generate_topology()

    @property
    def center_line(self):
        return 5

    @property
    def boundary_left_down(self):
        return 6

    @property
    def boundary_right_down(self):
        return 7

    @property
    def boundary_down(self):
        return 8

    @property
    def boundary_left_up(self):
        return 9

    @property
    def boundary_up(self):
        return 10

    @property
    def boundary_right_up(self):
        return 11

    @property
    def size(self):
        return self._size