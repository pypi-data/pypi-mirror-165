import gmsh
import math
import numpy as np

# todo: Two physical group must be redesign.
class PhysicalFieldBase:
    def __init__(self, mesh):
        self._cell_info = None
        self._face_info = np.zeros([mesh.face_num, 3], dtype=np.float32)
        self._initial_condition = np.zeros(mesh.cell_num, dtype=np.float32)
        self._mesh = mesh
        self._name = None

        self._physical_group_info = {}

    def generate_info(self):
        self.__calc_face_info()
        self.__calc_cell_info()

    def get_physical_properties(self, number):
        iterations = 0
        for key in self._physical_group_info:
            if key[0] == self._mesh.dim:
                if iterations == number:
                    return self._physical_group_info[key]
                else:
                    iterations += 1

    def set_boundary_as_dirichlet(self, boundaries, info):
        physical_group_dim_tag = (self._mesh.dim - 1, gmsh.model.add_physical_group(self._mesh.dim - 1, boundaries))
        self._physical_group_info[physical_group_dim_tag] = [1, info, 0]

    def set_boundary_as_periodic(self, boundaries):
        """
        This periodic interface only support translation type periodic boundaries.
        :param boundaries:
        :return:
        """
        assert len(boundaries) == 2

        # todo: 这个提炼一个提取点的函数，检测是不是均值更准一点。
        # Calculate center coordinate of boundaries 0.
        upward, downward = gmsh.model.get_adjacencies(self._mesh.dim - 1, boundaries[0])
        tuple0 = gmsh.model.get_bounding_box(self._mesh.dim - 2, downward[0])
        tuple1 = gmsh.model.get_bounding_box(self._mesh.dim - 2, downward[1])
        center = np.zeros(3, dtype=np.float64)
        center[0] = (tuple0[0] + tuple0[3] + tuple1[0] + tuple1[3]) / 4
        center[1] = (tuple0[1] + tuple0[4] + tuple1[1] + tuple1[4]) / 4
        center[2] = (tuple0[2] + tuple0[5] + tuple1[2] + tuple1[5]) / 4
        # Calculate center coordinate of boundaries 1.
        upward, downward = gmsh.model.get_adjacencies(self._mesh.dim - 1, boundaries[1])
        tuple0 = gmsh.model.get_bounding_box(self._mesh.dim - 2, downward[0])
        tuple1 = gmsh.model.get_bounding_box(self._mesh.dim - 2, downward[1])
        center[0] -= (tuple0[0] + tuple0[3] + tuple1[0] + tuple1[3]) / 4
        center[1] -= (tuple0[1] + tuple0[4] + tuple1[1] + tuple1[4]) / 4
        center[2] -= (tuple0[2] + tuple0[5] + tuple1[2] + tuple1[5]) / 4

        affine = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.float64)
        affine[3] = center[0]
        affine[7] = center[1]
        affine[11] = center[2]
        gmsh.model.mesh.set_periodic(self._mesh.dim - 1, [boundaries[0]], [boundaries[1]], affine)

        physical_group_dim_tag = (self._mesh.dim - 1, gmsh.model.add_physical_group(self._mesh.dim - 1, boundaries))
        self._physical_group_info[physical_group_dim_tag] = [4, boundaries[0], 0]

    def set_initial_condition_by_scalar(self, value):
        self._initial_condition *= 0
        self._initial_condition += value

    def set_initial_condition_by_func(self, func):
        for i in range(self._mesh.cell_num):
            self._initial_condition[i] = func(self._mesh.cell_center[i])

    def set_name(self, name):
        self._name = name

    def set_physical_properties(self, areas, property_value_list):
        assert False

    def set_point_source(self, points, value):
        physical_group_dim_tag = (0, gmsh.model.add_physical_group(0, points))
        self._physical_group_info[physical_group_dim_tag] = value

    def __calc_boundary_dirichlet_2d(self, physical_group_dim_tag):
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
                node_s = self._mesh.nodes[node_tags[0]]
                node_e = self._mesh.nodes[node_tags[-1]]
                if np.linalg.norm(node_e) < np.linalg.norm(node_s):
                    node_e, node_s = node_s, node_e
                line_length = np.linalg.norm(node_e - node_s)

                if physical_group_info[1] == "cos":
                    for face_tag in face_tags:
                        percent = np.linalg.norm(self._mesh.face_center[face_tag] - node_s) / line_length
                        self._face_info[face_tag] = [physical_group_info[0], math.cos(percent * 2 * math.pi), 0]
                else:
                    assert False
            else:
                assert False

    def __calc_boundary_periodic_2d(self, physical_group_dim_tag):
        """
        [4, periodic_face, periodic_cell]
        :param physical_group_dim_tag:
        :return:
        """

        physical_group_info = self._physical_group_info[physical_group_dim_tag]
        master_tag, nodes, master_nodes, affine = gmsh.model.mesh.get_periodic_nodes(1, physical_group_info[1])
        face_num = len(nodes) - 1

        # Reset start and end point location.
        distance_02 = np.linalg.norm(self._mesh.nodes[int(nodes[0]) - 1] - self._mesh.nodes[int(nodes[2]) - 1])
        distance_12 = np.linalg.norm(self._mesh.nodes[int(nodes[1]) - 1] - self._mesh.nodes[int(nodes[2]) - 1])
        if distance_02 < distance_12:
            nodes[0], nodes[1] = nodes[1], nodes[0]
            master_nodes[0], master_nodes[1] = master_nodes[1], master_nodes[0]
        # Move start point to the end, because the node order is reverse.
        for i in range(face_num):
            nodes[i], nodes[i + 1] = nodes[i + 1], nodes[i]
            master_nodes[i], master_nodes[i + 1] = master_nodes[i + 1], master_nodes[i]

        # Assign face_info.
        for i in range(face_num):
            tag_face, unuse = gmsh.model.mesh.get_edges([nodes[i], nodes[i + 1]])
            tag_master_face, unuse = gmsh.model.mesh.get_edges([master_nodes[i], master_nodes[i + 1]])
            self._face_info[tag_face - 1, 0] = 4
            self._face_info[tag_face - 1, 1] = tag_master_face - 1
            self._face_info[tag_face - 1, 2] = self._mesh.face_cell[tag_master_face - 1, 0]
            self._face_info[tag_master_face - 1, 0] = 4
            self._face_info[tag_master_face - 1, 1] = tag_face - 1
            self._face_info[tag_master_face - 1, 2] = self._mesh.face_cell[tag_face - 1, 0]

    def __calc_cell_info(self):
        self.__calc_point_source()
        self.__calc_physical_properties()

    def __calc_face_info(self):
        face_group_dim_tags = gmsh.model.get_physical_groups(dim=self._mesh.dim-1)
        for dim_tag in face_group_dim_tags:
            if self._physical_group_info[dim_tag][0] == 1:
                self.__calc_boundary_dirichlet_2d(dim_tag)
            elif self._physical_group_info[dim_tag][0] == 4:
                self.__calc_boundary_periodic_2d(dim_tag)
            else:
                assert False

    def __calc_physical_properties(self):
        cell_group_dim_tags = gmsh.model.get_physical_groups(dim=self._mesh.dim)

        for dim_tag in cell_group_dim_tags:
            physical_properties = self._physical_group_info[dim_tag][-1]

            # Get all entities of this source.
            entity_dim_tags = gmsh.model.get_entities_for_physical_group(dim_tag[0], dim_tag[1])

            for entity_dim_tag in entity_dim_tags:
                element_tags, _ = gmsh.model.mesh.get_elements_by_type(self._mesh.gmsh_element_type)
                # Here, element tags include point element and face elements, so cell tags are not start from zero.
                element_tags -= element_tags[0]

                for element_tag in element_tags:
                    self._cell_info[element_tag, 1::] = physical_properties

    def __calc_point_source(self):
        point_source_dim_tags = gmsh.model.get_physical_groups(dim=0)

        for dim_tag in point_source_dim_tags:
            source_value = self._physical_group_info[dim_tag]

            # Get all points of this source.
            entity_tags = gmsh.model.get_entities_for_physical_group(dim_tag[0], dim_tag[1])

            for entity_tag in entity_tags:
                node_tags, _, _ = gmsh.model.mesh.get_nodes(0, entity_tag)

                # todo: Here can separate out a distribute method function.
                for node in node_tags:
                    related_cell = []
                    for i in range(self._mesh.cell_num):
                        for j in range(self._mesh.node_per_cell):
                            if self._mesh.cells[i, j] + 1 == node:
                                related_cell.append(i)
                                break
                    source_each_cell = source_value / len(related_cell)

                    for cell in related_cell:
                        self._cell_info[cell, 0] += source_each_cell

    @property
    def cell_info(self):
        return self._cell_info

    @property
    def face_info(self):
        return self._face_info

    @property
    def initial_condition(self):
        return self._initial_condition

    @property
    def name(self):
        return self._name