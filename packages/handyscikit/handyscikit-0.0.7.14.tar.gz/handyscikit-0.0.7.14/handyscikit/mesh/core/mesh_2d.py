from .mesh_base import MeshBase
import gmsh
import math
import numpy as np


class Mesh2D(MeshBase):
    def __init__(self):
        MeshBase.__init__(self)

    def _calc_face_area(self):
        self._face_area = np.zeros([self._face_num], dtype=np.float32)

        for i in range(self.face_num):
            self._face_area[i] = np.linalg.norm(self._nodes[self._faces[i,0]] - self._nodes[self._faces[i, 1]])

    def _calc_face_center(self):
        self._face_center = np.zeros([self._face_num, 3], dtype=np.float32)

        for i in range(self._face_num):
            self._face_center[i] = (self._nodes[self._faces[i,0]] + self._nodes[self._faces[i,1]])/2

    def _calc_face_norm(self):
        self._face_norm = np.zeros([self._face_num, 3], dtype=np.float32)

        for i in range(self._face_num):
            node0 = self._nodes[self._faces[i, 0]]
            node1 = self._nodes[self._faces[i, 1]]
            if node0[1] - node1[1] == 0:
                self._face_norm[i, 1] = 1
            else:
                tmp = (node0[0] - node1[0])/(node1[1] - node0[1])
                self._face_norm[i, 0] = 1/(1 + tmp**2)**0.5
                self._face_norm[i, 1] = tmp/(1 + tmp**2)**0.5
            if np.dot(self._face_norm[i], self._cell_center[self._face_cell[i, 0]] - self._face_center[i]) > 0:
                self._face_norm[i] *= -1

    def _make_faces_and_cell_face(self):
        gmsh.model.mesh.create_edges()

        element_node_tags = gmsh.model.mesh.get_element_edge_nodes(self._gmsh_element_type)
        element_node_num = element_node_tags.size

        (face_tags, unuse) = gmsh.model.mesh.get_edges(element_node_tags)  # Inner face repeated in face tags.
        element_face_num = face_tags.size

        # Calculate face number.
        self._face_num = 0
        tmp = np.full(element_face_num, fill_value=-1)
        for i in range(element_face_num):
            if tmp[face_tags[i]] == -1:
                tmp[face_tags[i]] = 0
                self._face_num += 1

        self._faces = np.zeros([self._face_num, self._node_per_face], dtype=np.int32)
        for i in range(element_node_num):
            self._faces[int(face_tags[i//2]-1), i%2] = element_node_tags[i]-1

        self._cell_face = face_tags.reshape([self._cell_num, self._face_per_cell])
        self._cell_face = self._cell_face.astype(np.int32)
        self._cell_face -= 1
