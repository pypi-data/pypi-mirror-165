from .mesh_base import MeshBase
import gmsh
import math
import numpy as np


class Mesh2D(MeshBase):
    def __init__(self):
        MeshBase.__init__(self)

    def _calculate_face_area(self):
        self._face_area = np.zeros([self._face_num], dtype=np.float32)

        for i in range(self.face_num):
            self._face_area[i] = np.linalg.norm(self._nodes[self._faces[i,0]] - self._nodes[self._faces[i, 1]])

    def _calculate_face_center(self):
        self._face_center = np.zeros([self._face_num, 3], dtype=np.float32)

        for i in range(self._face_num):
            self._face_center[i] = (self._nodes[self._faces[i,0]] + self._nodes[self._faces[i,1]])/2

    def _calculate_face_info(self):
        self._face_info = np.zeros([self._face_num, 3], dtype=np.float32)

        physical_group_dim_tags = gmsh.model.get_physical_groups(dim=self._dim-1)
        for dim_tag in physical_group_dim_tags:
            if self._physical_group_info[dim_tag][0] == 1:
                self._deal_dirichlet_face(dim_tag)
            elif self._physical_group_info[dim_tag][0] == 4:
                self._deal_periodic_face(dim_tag)
            else:
                assert False

    def _calculate_face_norm(self):
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

    def _deal_dirichlet_face(self, physical_group_dim_tag):
        physical_group_info = self._physical_group_info[physical_group_dim_tag]
        entity_tags = gmsh.model.get_entities_for_physical_group(physical_group_dim_tag[0], physical_group_dim_tag[1])

        for entity_tag in entity_tags:
            node_tags = gmsh.model.mesh.get_element_edge_nodes(1, entity_tag)  # 1 means line element.

            # Node tag in gmsh starts from 1, however, index starts from zero.
            face_tags, unuse = gmsh.model.mesh.get_edges(node_tags)
            face_tags -= 1
            node_tags -= 1

            if isinstance(physical_group_info[1], float) or isinstance(physical_group_info[1], int):
                for face_tag in face_tags:
                    self._face_info[face_tag] = physical_group_info
            elif isinstance(physical_group_info[1], str):
                # todo: In this condition, only straight line can be used.
                node_s = self._nodes[node_tags[0]]
                node_e = self._nodes[node_tags[-1]]
                if np.linalg.norm(node_e) < np.linalg.norm(node_s):
                    node_e, node_s = node_s, node_e
                line_length = np.linalg.norm(node_e - node_s)

                if physical_group_info[1] == "cos":
                    for face_tag in face_tags:
                        percent = np.linalg.norm(self._face_center[face_tag] - node_s) / line_length
                        self._face_info[face_tag] = [physical_group_info[0], math.cos(percent * 2 * math.pi), 0]
                else:
                    assert False
            else:
                assert False

    def _deal_periodic_face(self, physical_group_dim_tag):
        """
        [4, periodic_face, periodic_cell]
        :param physical_group_dim_tag:
        :return:
        """
        physical_group_info = self._physical_group_info[physical_group_dim_tag]
        master_tag, nodes, master_nodes, affine = gmsh.model.mesh.get_periodic_nodes(1, physical_group_info[1])
        face_num = len(nodes) - 1

        # Reset start and end point location.
        distance_02 = np.linalg.norm(self._nodes[int(nodes[0])-1] - self._nodes[int(nodes[2])-1])
        distance_12 = np.linalg.norm(self._nodes[int(nodes[1])-1] - self._nodes[int(nodes[2])-1])
        if distance_02 < distance_12:
            nodes[0], nodes[1] = nodes[1], nodes[0]
            master_nodes[0], master_nodes[1] = master_nodes[1], master_nodes[0]
        # Move start point to the end, because the node order is reverse.
        for i in range(face_num):
            nodes[i], nodes[i+1] = nodes[i+1], nodes[i]
            master_nodes[i], master_nodes[i+1] = master_nodes[i+1], master_nodes[i]

        # Assign face_info.
        for i in range(face_num):
            tag_face, unuse = gmsh.model.mesh.get_edges([nodes[i], nodes[i+1]])
            tag_master_face, unuse = gmsh.model.mesh.get_edges([master_nodes[i], master_nodes[i+1]])
            self._face_info[tag_face-1, 0] = 4
            self._face_info[tag_face-1, 1] = tag_master_face-1
            self._face_info[tag_face-1, 2] = self._face_cell[tag_master_face-1, 0]
            self._face_info[tag_master_face-1, 0] = 4
            self._face_info[tag_master_face-1, 1] = tag_face-1
            self._face_info[tag_master_face-1, 2] = self._face_cell[tag_face-1, 0]

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