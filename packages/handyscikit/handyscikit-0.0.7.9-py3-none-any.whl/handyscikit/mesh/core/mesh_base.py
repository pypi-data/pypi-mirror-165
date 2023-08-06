from ...common.print_related import cprint
import gmsh
import math
import numpy as np
import time


class MeshBase:
    def __init__(self):
        if not gmsh.is_initialized(): gmsh.initialize()
        gmsh.option.set_number("General.Terminal", 0)

        self._cell_num = None
        self._dim = None
        self._face_num = None
        self._face_per_cell = None
        self._node_num = None
        self._node_per_cell = None
        self._node_per_face = None

        self._cell_cell = None
        self._cell_volume = None
        self._cell_face = None
        self._cell_center = None
        self._cells = None
        self._face_area = None
        self._face_cell = None
        self._face_center = None
        self._face_info = None
        self._face_norm = None
        self._faces = None
        self._nodes = None

        self._gmsh_element_type = None

    def clear_gmsh(self):
        # todo: Using gmsh model to offset the influence between different models.
        gmsh.clear()

    def _calc_face_area(self):
        assert False

    def _calc_face_center(self):
        assert False

    def _calc_face_norm(self):
        assert False

    def _generate_topology(self):
        self.__make_nodes()
        self.__make_cells()
        self._make_faces_and_cell_face()
        self.__make_other_relationships()

        self.__calc_cell_center()
        self.__calc_cell_volume()
        self._calc_face_area()
        self._calc_face_center()
        self._calc_face_norm()

    def _make_faces_and_cell_face(self):
        assert False

    def __make_cells(self):
        (cell_tags, node_tags) = gmsh.model.mesh.get_elements_by_type(self._gmsh_element_type)  # 3 means quadrilateral.
        self._cells = node_tags.reshape([-1, self._node_per_cell])
        self._cells = self._cells.astype(np.int32)
        self._cells -= 1  # Gmsh cells index starts from 1, but index start from zero, transfer it.
        self._cell_num = self._cells.shape[0]

    def __make_nodes(self):
        (node_tags, node_coordinates, unuse) = gmsh.model.mesh.get_nodes()
        self._node_num = node_tags.size
        self._nodes = node_coordinates.reshape([-1, 3])
        self._nodes = self._nodes.astype(np.float32)

    def __make_other_relationships(self):
        self._face_cell = np.full([self._face_num, 2], fill_value=-1, dtype=np.int32)
        for i in range(self._cell_num):
            for j in range(self._face_per_cell):
                if self._face_cell[self._cell_face[i, j], 0] == -1:
                    self._face_cell[self._cell_face[i, j], 0] = i
                else:
                    self._face_cell[self._cell_face[i, j], 1] = i

        self._cell_cell = np.full([self._cell_num, self._face_per_cell], fill_value=-1, dtype=np.int32)
        for i in range(self._face_num):
            if self._face_cell[i, 0] != -1 and self._face_cell[i, 1] != -1:
                for j in range(self._face_per_cell):
                    if self._cell_cell[self._face_cell[i, 0], j] == -1:
                        self._cell_cell[self._face_cell[i, 0], j] = self._face_cell[i, 1]
                        break
                for j in range(self._face_per_cell):
                    if self._cell_cell[self._face_cell[i, 1], j] == -1:
                        self._cell_cell[self._face_cell[i, 1], j] = self._face_cell[i, 0]
                        break

    def __calc_cell_center(self):
        self._cell_center = np.zeros([self._cell_num, 3], dtype=np.float32)

        for i in range(self._cell_num):
            for j in range(self._node_per_cell):
                self._cell_center[i] += self._nodes[self._cells[i, j]]
            self._cell_center[i] /= self._node_per_cell

    def __calc_cell_volume(self):
        self._cell_volume = np.zeros([self._cell_num], dtype=np.float32)

        if self._gmsh_element_type == 3:
            for i in range(self._cell_num):
                vector_0 = self._nodes[self._cells[i, 0]] - self._nodes[self._cells[i, 1]]
                vector_1 = self._nodes[self._cells[i, 0]] - self._nodes[self._cells[i, 3]]
                self._cell_volume[i] = abs(np.cross(vector_0, vector_1)[2])  # 3D vector cross makes a new vector.
        elif self._gmsh_element_type == 2:
            for i in range(self.cell_num):
                node_0 = self._nodes[self._cells[i, 0]]
                node_1 = self._nodes[self._cells[i, 1]]
                node_2 = self._nodes[self._cells[i, 2]]
                self._cell_volume[i] = ((node_1[0] - node_0[0])*(node_2[1] - node_0[1]) -
                                        (node_1[1] - node_0[1])*(node_2[0] - node_0[0]))/2
        else:
            self._cell_volume = None

    @property
    def cell_cell(self):
        return self._cell_cell

    @property
    def cell_center(self):
        return self._cell_center

    @property
    def cell_face(self):
        return self._cell_face

    @property
    def cell_num(self):
        return self._cell_num

    @property
    def cell_volume(self):
        return self._cell_volume

    @property
    def cells(self):
        return self._cells

    @property
    def dim(self):
        return self._dim

    @property
    def face_cell(self):
        return self._face_cell

    @property
    def face_center(self):
        return self._face_center

    @property
    def face_area(self):
        return self._face_area

    @property
    def face_norm(self):
        return self._face_norm

    @property
    def face_num(self):
        return self._face_num

    @property
    def face_per_cell(self):
        return self._face_per_cell

    @property
    def faces(self):
        return self._faces

    @property
    def gmsh_element_type(self):
        return self._gmsh_element_type

    @property
    def node_num(self):
        return self._node_num

    @property
    def node_per_cell(self):
        return self._node_per_cell

    @property
    def node_per_face(self):
        return self._node_per_face

    @property
    def nodes(self):
        return self._nodes


def meshing_timer(func):
    def wrapper_func(*args, **kwargs):
        cprint("[handyscikit | Mesh] Meshing start.", color="purple")
        start_time = time.time()

        func(*args, **kwargs)

        spend_time = time.time() - start_time
        cprint("[handyscikit | Mesh] Meshing finished and takes %f seconds." % (spend_time), color="purple")

    return wrapper_func