from handyscikit import cprint
from handyscikit.mesh import CircleCase
from handyscikit.mesh import General2DCase
from handyscikit.mesh import RectangleCase
from handyscikit.mesh import SquareCase
from handyscikit.mesh import SingleFractureCase
import gmsh
import numpy as np


class CaseTest:
    @staticmethod
    def rectangle_case():
        mesh = RectangleCase([2, 1])
        mesh.set_dirichlet_boundary([mesh.boundary_up], 1)
        mesh.set_dirichlet_boundary([mesh.boundary_down], 2)
        mesh.set_dirichlet_boundary([mesh.boundary_left], 3)
        mesh.set_dirichlet_boundary([mesh.boundary_right], 4)
        mesh.generate_structured([3, 3], show_mesh=False)

        assert mesh.dim == 2

        assert mesh.node_per_face == 2

        assert mesh.node_num == 16

        assert mesh.size == [2, 1]

        assert mesh.structured_num == [3, 3]

        assert mesh.face_per_cell == 4

        assert mesh.node_per_cell == 4

        assert mesh.boundary_down == 1 and mesh.boundary_right == 2 and mesh.boundary_up == 3 and \
               mesh.boundary_left == 4

        cprint("[SquareCase Test] Case related attribute test passed.", color="green")

    @staticmethod
    def circle_case():
        mesh = CircleCase(1)
        mesh.set_dirichlet_boundary([mesh.boundary], 1)
        mesh.generate_unstructured([1], show_mesh=False)

        assert mesh.dim == 2

        assert mesh.node_per_face == 2

        assert mesh.face_per_cell == 3

        assert mesh.node_per_cell == 3

        assert mesh.boundary == 1

        cprint("[CircelCase Test] Case related attribute test passed.", color="green")

    @staticmethod
    def single_fracture_case():
        mesh = SingleFractureCase([2, 1])
        mesh.set_dirichlet_boundary([mesh.boundary_up], 1)
        mesh.set_dirichlet_boundary([mesh.boundary_down], 2)
        mesh.set_dirichlet_boundary([mesh.boundary_left_down], 3)
        mesh.set_dirichlet_boundary([mesh.boundary_right_down], 4)
        mesh.set_fracture_mesh_size(0.01)
        mesh.set_mean_size(0.05)
        mesh.generate_unstructured(show_mesh=False)

        assert mesh.dim == 2

        assert mesh.node_per_face == 2

        assert mesh.size == [2, 1]

        assert mesh.face_per_cell == 3

        assert mesh.node_per_cell == 3

        assert mesh.center_line == 5 and mesh.boundary_left_down == 6 and mesh.boundary_right_down == 7 and \
               mesh.boundary_down == 8 and mesh.boundary_left_up == 9 and mesh.boundary_up == 10 and \
               mesh.boundary_right_up == 11

        cprint("[SingleFractureCase Test] Case related attribute test passed.", color="green")


class Mesh2DTest:
    @staticmethod
    def general_2d_test():
        mesh = General2DCase()
        mesh.geom.add_rectangle(-250, -250, 0, 500, 500)
        mesh.geom.add_point(0, 0, 0)
        mesh.geom.fragment([(0, 5)], [(2, 1)])
        mesh.geom.synchronize(show_geom=False)
        mesh.mesh.set_size([(0, 5), (0, 6), (0, 7), (0, 8), (0, 9)], 10)
        mesh.generate_unstructured(show_mesh=True)
        mesh.clear_gmsh()

        cprint("[General2D Test] General 2D can simply use.", color="green")

    @staticmethod
    def structured_quadrilateral_topology_test():
        mesh = SquareCase(1)
        mesh.generate_structured([2, 2])
        mesh.clear_gmsh()

        assert mesh.cell_cell[0, 0] == 2 and mesh.cell_cell[0, 1] == 1 and mesh.cell_cell[0, 2] == -1 and \
               mesh.cell_cell[0, 3] == -1
        assert mesh.cell_cell[1, 0] == 0 and mesh.cell_cell[1, 1] == 3 and mesh.cell_cell[1, 2] == -1 and \
               mesh.cell_cell[1, 3] == -1
        assert mesh.cell_cell[2, 0] == 0 and mesh.cell_cell[2, 1] == 3 and mesh.cell_cell[2, 2] == -1 and \
               mesh.cell_cell[2, 3] == -1
        assert mesh.cell_cell[3, 0] == 1 and mesh.cell_cell[3, 1] == 2 and mesh.cell_cell[3, 2] == -1 and \
               mesh.cell_cell[3, 3] == -1

        assert mesh.cell_center[0, 0] == 0.25 and mesh.cell_center[0, 1] == 0.25
        assert mesh.cell_center[1, 0] == 0.25 and mesh.cell_center[1, 1] == 0.75
        assert mesh.cell_center[2, 0] == 0.75 and mesh.cell_center[2, 1] == 0.25
        assert mesh.cell_center[3, 0] == 0.75 and mesh.cell_center[3, 1] == 0.75

        assert mesh.cell_face[0, 0] == 0 and mesh.cell_face[0, 1] == 8 and mesh.cell_face[0, 2] == 9 and \
               mesh.cell_face[0, 3] == 7
        assert mesh.cell_face[1, 0] == 9 and mesh.cell_face[1, 1] == 10 and mesh.cell_face[1, 2] == 5 and \
               mesh.cell_face[1, 3] == 6
        assert mesh.cell_face[2, 0] == 1 and mesh.cell_face[2, 1] == 2 and mesh.cell_face[2, 2] == 11 and \
               mesh.cell_face[2, 3] == 8
        assert mesh.cell_face[3, 0] == 11 and mesh.cell_face[3, 1] == 3 and mesh.cell_face[3, 2] == 4 and \
               mesh.cell_face[3, 3] == 10

        assert np.all(mesh.cell_volume == 0.25)
        assert mesh.cell_num == 4

        assert mesh.cells[0, 0] == 0 and mesh.cells[0, 1] == 4 and mesh.cells[0, 2] == 8 and mesh.cells[0, 3] == 7
        assert mesh.cells[1, 0] == 7 and mesh.cells[1, 1] == 8 and mesh.cells[1, 2] == 6 and mesh.cells[1, 3] == 3
        assert mesh.cells[2, 0] == 4 and mesh.cells[2, 1] == 1 and mesh.cells[2, 2] == 5 and mesh.cells[2, 3] == 8
        assert mesh.cells[3, 0] == 8 and mesh.cells[3, 1] == 5 and mesh.cells[3, 2] == 2 and mesh.cells[3, 3] == 6

        assert mesh.dim == 2

        assert mesh.face_cell[0, 0] == 0 and mesh.face_cell[0, 1] == -1
        assert mesh.face_cell[1, 0] == 2 and mesh.face_cell[1, 1] == -1
        assert mesh.face_cell[2, 0] == 2 and mesh.face_cell[2, 1] == -1
        assert mesh.face_cell[3, 0] == 3 and mesh.face_cell[3, 1] == -1
        assert mesh.face_cell[4, 0] == 3 and mesh.face_cell[4, 1] == -1
        assert mesh.face_cell[5, 0] == 1 and mesh.face_cell[5, 1] == -1
        assert mesh.face_cell[6, 0] == 1 and mesh.face_cell[6, 1] == -1
        assert mesh.face_cell[7, 0] == 0 and mesh.face_cell[7, 1] == -1
        assert mesh.face_cell[8, 0] == 0 and mesh.face_cell[8, 1] == 2
        assert mesh.face_cell[9, 0] == 0 and mesh.face_cell[9, 1] == 1
        assert mesh.face_cell[10, 0] == 1 and mesh.face_cell[10, 1] == 3
        assert mesh.face_cell[11, 0] == 2 and mesh.face_cell[11, 1] == 3

        assert mesh.face_center[0, 0] == 0.25 and mesh.face_center[0, 1] == 0.0
        assert mesh.face_center[1, 0] == 0.75 and mesh.face_center[1, 1] == 0.0
        assert mesh.face_center[2, 0] == 1.0 and mesh.face_center[2, 1] == 0.25
        assert mesh.face_center[3, 0] == 1.0 and mesh.face_center[3, 1] == 0.75
        assert mesh.face_center[4, 0] == 0.75 and mesh.face_center[4, 1] == 1.0
        assert mesh.face_center[5, 0] == 0.25 and mesh.face_center[5, 1] == 1.0
        assert mesh.face_center[6, 0] == 0.0 and mesh.face_center[6, 1] == 0.75
        assert mesh.face_center[7, 0] == 0.0 and mesh.face_center[7, 1] == 0.25
        assert mesh.face_center[8, 0] == 0.5 and mesh.face_center[8, 1] == 0.25
        assert mesh.face_center[9, 0] == 0.25 and mesh.face_center[9, 1] == 0.5
        assert mesh.face_center[10, 0] == 0.5 and mesh.face_center[10, 1] == 0.75
        assert mesh.face_center[11, 0] == 0.75 and mesh.face_center[11, 1] == 0.5

        assert mesh.face_norm[0, 0] == 0.0 and mesh.face_norm[0, 1] == -1.0
        assert mesh.face_norm[1, 0] == 0.0 and mesh.face_norm[1, 1] == -1.0
        assert mesh.face_norm[2, 0] == 1.0 and mesh.face_norm[2, 1] == 0.0
        assert mesh.face_norm[3, 0] == 1.0 and mesh.face_norm[3, 1] == 0.0
        assert mesh.face_norm[4, 0] == 0.0 and mesh.face_norm[4, 1] == 1.0
        assert mesh.face_norm[5, 0] == 0.0 and mesh.face_norm[5, 1] == 1.0
        assert mesh.face_norm[6, 0] == -1.0 and mesh.face_norm[6, 1] == 0.0
        assert mesh.face_norm[7, 0] == -1.0 and mesh.face_norm[7, 1] == 0.0
        assert mesh.face_norm[8, 0] == 1.0 and mesh.face_norm[8, 1] == 0.0
        assert mesh.face_norm[9, 0] == 0.0 and mesh.face_norm[9, 1] == 1.0
        assert mesh.face_norm[10, 0] == 1.0 and mesh.face_norm[10, 1] == 0.0
        assert mesh.face_norm[11, 0] == 0.0 and mesh.face_norm[11, 1] == 1.0

        assert mesh.face_num == 12
        assert np.all(mesh.face_area == 0.5)

        assert mesh.faces[0, 0] == 0 and mesh.faces[0, 1] == 4
        assert mesh.faces[1, 0] == 4 and mesh.faces[1, 1] == 1
        assert mesh.faces[2, 0] == 1 and mesh.faces[2, 1] == 5
        assert mesh.faces[3, 0] == 5 and mesh.faces[3, 1] == 2
        assert mesh.faces[4, 0] == 2 and mesh.faces[4, 1] == 6
        assert mesh.faces[5, 0] == 6 and mesh.faces[5, 1] == 3
        assert mesh.faces[6, 0] == 3 and mesh.faces[6, 1] == 7
        assert mesh.faces[7, 0] == 7 and mesh.faces[7, 1] == 0
        assert mesh.faces[8, 0] == 8 and mesh.faces[8, 1] == 4
        assert mesh.faces[9, 0] == 7 and mesh.faces[9, 1] == 8
        assert mesh.faces[10, 0] == 6 and mesh.faces[10, 1] == 8
        assert mesh.faces[11, 0] == 8 and mesh.faces[11, 1] == 5

        assert mesh.node_num == 9

        assert mesh.nodes[0, 0] == 0.0 and mesh.nodes[0, 1] == 0.0
        assert mesh.nodes[1, 0] == 1.0 and mesh.nodes[1, 1] == 0.0
        assert mesh.nodes[2, 0] == 1.0 and mesh.nodes[2, 1] == 1.0
        assert mesh.nodes[3, 0] == 0.0 and mesh.nodes[3, 1] == 1.0
        assert mesh.nodes[4, 0] == 0.5 and mesh.nodes[4, 1] == 0.0
        assert mesh.nodes[5, 0] == 1.0 and mesh.nodes[5, 1] == 0.5
        assert mesh.nodes[6, 0] == 0.5 and mesh.nodes[6, 1] == 1.0
        assert mesh.nodes[7, 0] == 0.0 and mesh.nodes[7, 1] == 0.5
        assert mesh.nodes[8, 0] == 0.5 and mesh.nodes[8, 1] == 0.5

        cprint("[SquareCase Test] Structured quadrilateral topology test passed.", color="green")

    @staticmethod
    def unstructured_triangle_topology_test():
        mesh = SquareCase(1)

        # Particular add four point for test in different os and differen gmsh version.
        point_tags = []
        point_tags.append(gmsh.model.occ.add_point(0.7386115, 0.26138848, 0.0, 0.5))
        point_tags.append(gmsh.model.occ.add_point(0.625, 0.625, 0.0, 0.5))
        point_tags.append(gmsh.model.occ.add_point(0.35747692, 0.35085642, 0.0, 0.5))
        point_tags.append(gmsh.model.occ.add_point(0.28125, 0.71875, 0.0, 0.5))
        gmsh.model.occ.fragment([(0, point_tags[0]), (0, point_tags[1]), (0, point_tags[2]), (0, point_tags[3])],
                                [(2, 1)])
        gmsh.model.occ.synchronize()

        gmsh.model.mesh.set_size([(0, 9)], 0.5)
        gmsh.model.mesh.set_size([(0, 10)], 0.5)
        gmsh.model.mesh.set_size([(0, 11)], 0.5)
        gmsh.model.mesh.set_size([(0, 12)], 0.5)
        # Uniqe deal finished.

        mesh.generate_unstructured([0.5, 0.5, 0.5, 0.5], show_mesh=False)
        mesh.clear_gmsh()

        error = 1e-6
        ghost_cell = -1

        assert mesh.cell_cell[0, 0] == 1 and mesh.cell_cell[0, 1] == 11 and mesh.cell_cell[0, 2] == ghost_cell
        assert mesh.cell_cell[1, 0] == 0 and mesh.cell_cell[1, 1] == 8 and mesh.cell_cell[1, 2] == ghost_cell
        assert mesh.cell_cell[2, 0] == 8 and mesh.cell_cell[2, 1] == 3 and mesh.cell_cell[2, 2] == ghost_cell
        assert mesh.cell_cell[3, 0] == 2 and mesh.cell_cell[3, 1] == 10 and mesh.cell_cell[3, 2] == ghost_cell
        assert mesh.cell_cell[4, 0] == 5 and mesh.cell_cell[4, 1] == 12 and mesh.cell_cell[4, 2] == ghost_cell
        assert mesh.cell_cell[5, 0] == 4 and mesh.cell_cell[5, 1] == 10 and mesh.cell_cell[5, 2] == ghost_cell
        assert mesh.cell_cell[6, 0] == 7 and mesh.cell_cell[6, 1] == 12 and mesh.cell_cell[6, 2] == ghost_cell
        assert mesh.cell_cell[7, 0] == 6 and mesh.cell_cell[7, 1] == 11 and mesh.cell_cell[7, 2] == ghost_cell
        assert mesh.cell_cell[8, 0] == 1 and mesh.cell_cell[8, 1] == 2 and mesh.cell_cell[8, 2] == 9
        assert mesh.cell_cell[9, 0] == 8 and mesh.cell_cell[9, 1] == 11 and mesh.cell_cell[9, 2] == 13
        assert mesh.cell_cell[10, 0] == 3 and mesh.cell_cell[10, 1] == 5 and mesh.cell_cell[10, 2] == 13
        assert mesh.cell_cell[11, 0] == 0 and mesh.cell_cell[11, 1] == 7 and mesh.cell_cell[11, 2] == 9
        assert mesh.cell_cell[12, 0] == 4 and mesh.cell_cell[12, 1] == 6 and mesh.cell_cell[12, 2] == 13
        assert mesh.cell_cell[13, 0] == 9 and mesh.cell_cell[13, 1] == 10 and mesh.cell_cell[13, 2] == 12

        assert abs(mesh.cell_center[0, 0] - 0.74620384) < error and abs(mesh.cell_center[0, 1] - 0.0871295) < error
        assert abs(mesh.cell_center[1, 0] - 0.91287047) < error and abs(mesh.cell_center[1, 1] - 0.25379616) < error
        assert abs(mesh.cell_center[2, 0] - 0.875) < error and abs(mesh.cell_center[2, 1] - 0.7083333) < error
        assert abs(mesh.cell_center[3, 0] - 0.7083333) < error and abs(mesh.cell_center[3, 1] - 0.875) < error
        assert abs(mesh.cell_center[4, 0] - 0.09375) < error and abs(mesh.cell_center[4, 1] - 0.7395833) < error
        assert abs(mesh.cell_center[5, 0] - 0.26041666) < error and abs(mesh.cell_center[5, 1] - 0.90625) < error
        assert abs(mesh.cell_center[6, 0] - 0.11915898) < error and abs(mesh.cell_center[6, 1] - 0.2836188) < error
        assert abs(mesh.cell_center[7, 0] - 0.28582564) < error and abs(mesh.cell_center[7, 1] - 0.11695214) < error
        assert abs(mesh.cell_center[8, 0] - 0.78787047) < error and abs(mesh.cell_center[8, 1] - 0.4621295) < error
        assert abs(mesh.cell_center[9, 0] - 0.57369614) < error and abs(mesh.cell_center[9, 1] - 0.41241494) < error
        assert abs(mesh.cell_center[10, 0] - 0.46875) < error and abs(mesh.cell_center[10, 1] - 0.78125) < error
        assert abs(mesh.cell_center[11, 0] - 0.53202945) < error and abs(mesh.cell_center[11, 1] - 0.20408164) < error
        assert abs(mesh.cell_center[12, 0] - 0.21290898) < error and abs(mesh.cell_center[12, 1] - 0.5232021) < error
        assert abs(mesh.cell_center[13, 0] - 0.42124233) < error and abs(mesh.cell_center[13, 1] - 0.5648688) < error

        assert mesh.cell_face[0, 0] == 1 and mesh.cell_face[0, 1] == 8 and mesh.cell_face[0, 2] == 9
        assert mesh.cell_face[1, 0] == 2 and mesh.cell_face[1, 1] == 10 and mesh.cell_face[1, 2] == 8
        assert mesh.cell_face[2, 0] == 11 and mesh.cell_face[2, 1] == 3 and mesh.cell_face[2, 2] == 12
        assert mesh.cell_face[3, 0] == 12 and mesh.cell_face[3, 1] == 4 and mesh.cell_face[3, 2] == 13
        assert mesh.cell_face[4, 0] == 14 and mesh.cell_face[4, 1] == 6 and mesh.cell_face[4, 2] == 15
        assert mesh.cell_face[5, 0] == 5 and mesh.cell_face[5, 1] == 14 and mesh.cell_face[5, 2] == 16
        assert mesh.cell_face[6, 0] == 7 and mesh.cell_face[6, 1] == 17 and mesh.cell_face[6, 2] == 18
        assert mesh.cell_face[7, 0] == 17 and mesh.cell_face[7, 1] == 0 and mesh.cell_face[7, 2] == 19
        assert mesh.cell_face[8, 0] == 10 and mesh.cell_face[8, 1] == 11 and mesh.cell_face[8, 2] == 20
        assert mesh.cell_face[9, 0] == 21 and mesh.cell_face[9, 1] == 20 and mesh.cell_face[9, 2] == 22
        assert mesh.cell_face[10, 0] == 13 and mesh.cell_face[10, 1] == 16 and mesh.cell_face[10, 2] == 23
        assert mesh.cell_face[11, 0] == 19 and mesh.cell_face[11, 1] == 9 and mesh.cell_face[11, 2] == 21
        assert mesh.cell_face[12, 0] == 15 and mesh.cell_face[12, 1] == 18 and mesh.cell_face[12, 2] == 24
        assert mesh.cell_face[13, 0] == 22 and mesh.cell_face[13, 1] == 23 and mesh.cell_face[13, 2] == 24

        assert abs(mesh.cell_volume[0] - 0.06534712) < error
        assert abs(mesh.cell_volume[1] - 0.06534712) < error
        assert abs(mesh.cell_volume[2] - 0.09375) < error
        assert abs(mesh.cell_volume[3] - 0.09375) < error
        assert abs(mesh.cell_volume[4] - 0.0703125) < error
        assert abs(mesh.cell_volume[5] - 0.0703125) < error
        assert abs(mesh.cell_volume[6] - 0.08936923) < error
        assert abs(mesh.cell_volume[7] - 0.08771411) < error
        assert abs(mesh.cell_volume[8] - 0.06107644) < error
        assert abs(mesh.cell_volume[9] - 0.06421017) < error
        assert abs(mesh.cell_volume[10] - 0.05859375) < error
        assert abs(mesh.cell_volume[11] - 0.06048614) < error
        assert abs(mesh.cell_volume[12] - 0.06007235) < error
        assert abs(mesh.cell_volume[13] - 0.05965857) < error

        assert mesh.cell_num == 14

        assert mesh.cells[0, 0] == 8 and mesh.cells[0, 1] == 5 and mesh.cells[0, 2] == 0
        assert mesh.cells[1, 0] == 5 and mesh.cells[1, 1] == 9 and mesh.cells[1, 2] == 0
        assert mesh.cells[2, 0] == 1 and mesh.cells[2, 1] == 9 and mesh.cells[2, 2] == 6
        assert mesh.cells[3, 0] == 1 and mesh.cells[3, 1] == 6 and mesh.cells[3, 2] == 10
        assert mesh.cells[4, 0] == 3 and mesh.cells[4, 1] == 7 and mesh.cells[4, 2] == 11
        assert mesh.cells[5, 0] == 10 and mesh.cells[5, 1] == 7 and mesh.cells[5, 2] == 3
        assert mesh.cells[6, 0] == 11 and mesh.cells[6, 1] == 4 and mesh.cells[6, 2] == 2
        assert mesh.cells[7, 0] == 2 and mesh.cells[7, 1] == 4 and mesh.cells[7, 2] == 8
        assert mesh.cells[8, 0] == 0 and mesh.cells[8, 1] == 9 and mesh.cells[8, 2] == 1
        assert mesh.cells[9, 0] == 2 and mesh.cells[9, 1] == 0 and mesh.cells[9, 2] == 1
        assert mesh.cells[10, 0] == 1 and mesh.cells[10, 1] == 10 and mesh.cells[10, 2] == 3
        assert mesh.cells[11, 0] == 2 and mesh.cells[11, 1] == 8 and mesh.cells[11, 2] == 0
        assert mesh.cells[12, 0] == 3 and mesh.cells[12, 1] == 11 and mesh.cells[12, 2] == 2
        assert mesh.cells[13, 0] == 2 and mesh.cells[13, 1] == 1 and mesh.cells[13, 2] == 3

        assert mesh.dim == 2

        assert abs(mesh.face_area[0] - 0.5) < error
        assert abs(mesh.face_area[1] - 0.5) < error
        assert abs(mesh.face_area[2] - 0.5) < error
        assert abs(mesh.face_area[3] - 0.5) < error
        assert abs(mesh.face_area[4] - 0.5) < error
        assert abs(mesh.face_area[5] - 0.5) < error
        assert abs(mesh.face_area[6] - 0.5) < error
        assert abs(mesh.face_area[7] - 0.5) < error
        assert abs(mesh.face_area[8] - 0.36965913) < error
        assert abs(mesh.face_area[9] - 0.35392004) < error
        assert abs(mesh.face_area[10] - 0.35392004) < error
        assert abs(mesh.face_area[11] - 0.3952847) < error
        assert abs(mesh.face_area[12] - 0.53033006) < error
        assert abs(mesh.face_area[13] - 0.3952847) < error
        assert abs(mesh.face_area[14] - 0.39774758) < error
        assert abs(mesh.face_area[15] - 0.35630482) < error
        assert abs(mesh.face_area[16] - 0.35630482) < error
        assert abs(mesh.face_area[17] - 0.5008892) < error
        assert abs(mesh.face_area[18] - 0.38734165) < error
        assert abs(mesh.face_area[19] - 0.37869915) < error
        assert abs(mesh.face_area[20] - 0.3809474) < error
        assert abs(mesh.face_area[21] - 0.3914947) < error
        assert abs(mesh.face_area[22] - 0.38304478) < error
        assert abs(mesh.face_area[23] - 0.35630482) < error
        assert abs(mesh.face_area[24] - 0.37570763) < error

        assert mesh.face_cell[0, 0] == 7 and mesh.face_cell[0, 1] == ghost_cell
        assert mesh.face_cell[1, 0] == 0 and mesh.face_cell[1, 1] == ghost_cell
        assert mesh.face_cell[2, 0] == 1 and mesh.face_cell[2, 1] == ghost_cell
        assert mesh.face_cell[3, 0] == 2 and mesh.face_cell[3, 1] == ghost_cell
        assert mesh.face_cell[4, 0] == 3 and mesh.face_cell[4, 1] == ghost_cell
        assert mesh.face_cell[5, 0] == 5 and mesh.face_cell[5, 1] == ghost_cell
        assert mesh.face_cell[6, 0] == 4 and mesh.face_cell[6, 1] == ghost_cell
        assert mesh.face_cell[7, 0] == 6 and mesh.face_cell[7, 1] == ghost_cell
        assert mesh.face_cell[8, 0] == 0 and mesh.face_cell[8, 1] == 1
        assert mesh.face_cell[9, 0] == 0 and mesh.face_cell[9, 1] == 11
        assert mesh.face_cell[10, 0] == 1 and mesh.face_cell[10, 1] == 8
        assert mesh.face_cell[11, 0] == 2 and mesh.face_cell[11, 1] == 8
        assert mesh.face_cell[12, 0] == 2 and mesh.face_cell[12, 1] == 3
        assert mesh.face_cell[13, 0] == 3 and mesh.face_cell[13, 1] == 10
        assert mesh.face_cell[14, 0] == 4 and mesh.face_cell[14, 1] == 5
        assert mesh.face_cell[15, 0] == 4 and mesh.face_cell[15, 1] == 12
        assert mesh.face_cell[16, 0] == 5 and mesh.face_cell[16, 1] == 10
        assert mesh.face_cell[17, 0] == 6 and mesh.face_cell[17, 1] == 7
        assert mesh.face_cell[18, 0] == 6 and mesh.face_cell[18, 1] == 12
        assert mesh.face_cell[19, 0] == 7 and mesh.face_cell[19, 1] == 11
        assert mesh.face_cell[20, 0] == 8 and mesh.face_cell[20, 1] == 9
        assert mesh.face_cell[21, 0] == 9 and mesh.face_cell[21, 1] == 11
        assert mesh.face_cell[22, 0] == 9 and mesh.face_cell[22, 1] == 13
        assert mesh.face_cell[23, 0] == 10 and mesh.face_cell[23, 1] == 13
        assert mesh.face_cell[24, 0] == 12 and mesh.face_cell[24, 1] == 13

        assert abs(mesh.face_center[0, 0] - 0.25) < error and abs(mesh.face_center[0, 1] - 0.0) < error
        assert abs(mesh.face_center[1, 0] - 0.75) < error and abs(mesh.face_center[1, 1] - 0.0) < error
        assert abs(mesh.face_center[2, 0] - 1.0) < error and abs(mesh.face_center[2, 1] - 0.25) < error
        assert abs(mesh.face_center[3, 0] - 1.0) < error and abs(mesh.face_center[3, 1] - 0.75) < error
        assert abs(mesh.face_center[4, 0] - 0.75) < error and abs(mesh.face_center[4, 1] - 1.0) < error
        assert abs(mesh.face_center[5, 0] - 0.25) < error and abs(mesh.face_center[5, 1] - 1.0) < error
        assert abs(mesh.face_center[6, 0] - 0.0) < error and abs(mesh.face_center[6, 1] - 0.75) < error
        assert abs(mesh.face_center[7, 0] - 0.0) < error and abs(mesh.face_center[7, 1] - 0.25) < error
        assert abs(mesh.face_center[8, 0] - 0.86930573) < error and abs(mesh.face_center[8, 1] - 0.13069424) < error
        assert abs(mesh.face_center[9, 0] - 0.61930573) < error and abs(mesh.face_center[9, 1] - 0.13069424) < error
        assert abs(mesh.face_center[10, 0] - 0.86930573) < error and abs(mesh.face_center[10, 1] - 0.38069424) < error
        assert abs(mesh.face_center[11, 0] - 0.8125) < error and abs(mesh.face_center[11, 1] - 0.5625) < error
        assert abs(mesh.face_center[12, 0] - 0.8125) < error and abs(mesh.face_center[12, 1] - 0.8125) < error
        assert abs(mesh.face_center[13, 0] - 0.5625) < error and abs(mesh.face_center[13, 1] - 0.8125) < error
        assert abs(mesh.face_center[14, 0] - 0.140625) < error and abs(mesh.face_center[14, 1] - 0.859375) < error
        assert abs(mesh.face_center[15, 0] - 0.140625) < error and abs(mesh.face_center[15, 1] - 0.609375) < error
        assert abs(mesh.face_center[16, 0] - 0.390625) < error and abs(mesh.face_center[16, 1] - 0.859375) < error
        assert abs(mesh.face_center[17, 0] - 0.17873846) < error and abs(mesh.face_center[17, 1] - 0.17542821) < error
        assert abs(mesh.face_center[18, 0] - 0.17873846) < error and abs(mesh.face_center[18, 1] - 0.4254282) < error
        assert abs(mesh.face_center[19, 0] - 0.42873847) < error and abs(mesh.face_center[19, 1] - 0.17542821) < error
        assert abs(mesh.face_center[20, 0] - 0.68180573) < error and abs(mesh.face_center[20, 1] - 0.44319424) < error
        assert abs(mesh.face_center[21, 0] - 0.5480442) < error and abs(mesh.face_center[21, 1] - 0.30612245) < error
        assert abs(mesh.face_center[22, 0] - 0.49123847) < error and abs(mesh.face_center[22, 1] - 0.4879282) < error
        assert abs(mesh.face_center[23, 0] - 0.453125) < error and abs(mesh.face_center[23, 1] - 0.671875) < error
        assert abs(mesh.face_center[24, 0] - 0.31936347) < error and abs(mesh.face_center[24, 1] - 0.5348032) < error

        assert abs(mesh.face_norm[0, 0] - 0.0) < error and abs(mesh.face_norm[0, 1] - (-1)) < error
        assert abs(mesh.face_norm[1, 0] - 0.0) < error and abs(mesh.face_norm[1, 1] - (-1)) < error
        assert abs(mesh.face_norm[2, 0] - 1.0) < error and abs(mesh.face_norm[2, 1] - 0.0) < error
        assert abs(mesh.face_norm[3, 0] - 1.0) < error and abs(mesh.face_norm[3, 1] - 0.0) < error
        assert abs(mesh.face_norm[4, 0] - 0.0) < error and abs(mesh.face_norm[4, 1] - 1.0) < error
        assert abs(mesh.face_norm[5, 0] - 0.0) < error and abs(mesh.face_norm[5, 1] - 1.0) < error
        assert abs(mesh.face_norm[6, 0] - (-1.0)) < error and abs(mesh.face_norm[6, 1] - 0.0) < error
        assert abs(mesh.face_norm[7, 0] - (-1.0)) < error and abs(mesh.face_norm[7, 1] - 0.0) < error
        assert abs(mesh.face_norm[8, 0] - 0.70710677) < error and abs(mesh.face_norm[8, 1] - 0.70710677) < error
        assert abs(mesh.face_norm[9, 0] - (-0.73855233)) < error and abs(mesh.face_norm[9, 1] - 0.6741961) < error
        assert abs(mesh.face_norm[10, 0] - (-0.6741961)) < error and abs(mesh.face_norm[10, 1] - 0.73855233) < error
        assert abs(mesh.face_norm[11, 0] - (-0.31622776)) < error and abs(mesh.face_norm[11, 1] - (-0.9486833)) < error
        assert abs(mesh.face_norm[12, 0] - (-0.70710677)) < error and abs(mesh.face_norm[12, 1] - 0.70710677) < error
        assert abs(mesh.face_norm[13, 0] - (-0.9486833)) < error and abs(mesh.face_norm[13, 1] - (-0.31622776)) < error
        assert abs(mesh.face_norm[14, 0] - 0.70710677) < error and abs(mesh.face_norm[14, 1] - 0.70710677) < error
        assert abs(mesh.face_norm[15, 0] - 0.6139406) < error and abs(mesh.face_norm[15, 1] - (-0.78935224)) < error
        assert abs(mesh.face_norm[16, 0] - 0.78935224) < error and abs(mesh.face_norm[16, 1] - (-0.6139406)) < error
        assert abs(mesh.face_norm[17, 0] - 0.70046717) < error and abs(mesh.face_norm[17, 1] - (-0.7136846)) < error
        assert abs(mesh.face_norm[18, 0] - 0.38504398) < error and abs(mesh.face_norm[18, 1] - 0.92289823) < error
        assert abs(mesh.face_norm[19, 0] - 0.9264779) < error and abs(mesh.face_norm[19, 1] - 0.3763491) < error
        assert abs(mesh.face_norm[20, 0] - (-0.95449275)) < error and abs(mesh.face_norm[20, 1] - (-0.29823416)) < error
        assert abs(mesh.face_norm[21, 0] - (-0.22852913)) < error and abs(mesh.face_norm[21, 1] - (-0.9735371)) < error
        assert abs(mesh.face_norm[22, 0] - (-0.7156959)) < error and abs(mesh.face_norm[22, 1] - (0.69841206)) < error
        assert abs(mesh.face_norm[23, 0] - (-0.2631174)) < error and abs(mesh.face_norm[23, 1] - (-0.9647638)) < error
        assert abs(mesh.face_norm[24, 0] - 0.97920173) < error and abs(mesh.face_norm[24, 1] - 0.20288894) < error

        assert mesh.face_num == 25

        assert mesh.faces[0, 0] == 4 and mesh.faces[0, 1] == 8
        assert mesh.faces[1, 0] == 8 and mesh.faces[1, 1] == 5
        assert mesh.faces[2, 0] == 5 and mesh.faces[2, 1] == 9
        assert mesh.faces[3, 0] == 9 and mesh.faces[3, 1] == 6
        assert mesh.faces[4, 0] == 6 and mesh.faces[4, 1] == 10
        assert mesh.faces[5, 0] == 10 and mesh.faces[5, 1] == 7
        assert mesh.faces[6, 0] == 7 and mesh.faces[6, 1] == 11
        assert mesh.faces[7, 0] == 11 and mesh.faces[7, 1] == 4
        assert mesh.faces[8, 0] == 0 and mesh.faces[8, 1] == 5
        assert mesh.faces[9, 0] == 8 and mesh.faces[9, 1] == 0
        assert mesh.faces[10, 0] == 0 and mesh.faces[10, 1] == 9
        assert mesh.faces[11, 0] == 9 and mesh.faces[11, 1] == 1
        assert mesh.faces[12, 0] == 1 and mesh.faces[12, 1] == 6
        assert mesh.faces[13, 0] == 1 and mesh.faces[13, 1] == 10
        assert mesh.faces[14, 0] == 7 and mesh.faces[14, 1] == 3
        assert mesh.faces[15, 0] == 3 and mesh.faces[15, 1] == 11
        assert mesh.faces[16, 0] == 10 and mesh.faces[16, 1] == 3
        assert mesh.faces[17, 0] == 2 and mesh.faces[17, 1] == 4
        assert mesh.faces[18, 0] == 11 and mesh.faces[18, 1] == 2
        assert mesh.faces[19, 0] == 2 and mesh.faces[19, 1] == 8
        assert mesh.faces[20, 0] == 0 and mesh.faces[20, 1] == 1
        assert mesh.faces[21, 0] == 0 and mesh.faces[21, 1] == 2
        assert mesh.faces[22, 0] == 2 and mesh.faces[22, 1] == 1
        assert mesh.faces[23, 0] == 1 and mesh.faces[23, 1] == 3
        assert mesh.faces[24, 0] == 3 and mesh.faces[24, 1] == 2

        assert mesh.node_num == 12

        assert abs(mesh.nodes[0, 0] - 0.7386115) < error and abs(mesh.nodes[0, 1] - 0.26138848) < error
        assert mesh.nodes[1, 0] == 0.625 and mesh.nodes[1, 1] == 0.625
        assert abs(mesh.nodes[2, 0] - 0.35747692) < error and abs(mesh.nodes[2, 1] - 0.35085642) < error
        assert abs(mesh.nodes[3, 0] - 0.28125) < error and abs(mesh.nodes[3, 1] - 0.71875) < error
        assert mesh.nodes[4, 0] == 0.0 and mesh.nodes[4, 1] == 0.0
        assert mesh.nodes[5, 0] == 1.0 and mesh.nodes[5, 1] == 0.0
        assert mesh.nodes[6, 0] == 1.0 and mesh.nodes[6, 1] == 1.0
        assert mesh.nodes[7, 0] == 0.0 and mesh.nodes[7, 1] == 1.0
        assert mesh.nodes[8, 0] == 0.5 and mesh.nodes[8, 1] == 0.0
        assert mesh.nodes[9, 0] == 1.0 and mesh.nodes[9, 1] == 0.5
        assert mesh.nodes[10, 0] == 0.5 and mesh.nodes[10, 1] == 1.0
        assert mesh.nodes[11, 0] == 0.0 and mesh.nodes[11, 1] == 0.5

        cprint("[SquareCase Test] Unstructured triangle topology test passed.", color="green")


if __name__ == "__main__":
    CaseTest.rectangle_case()
    CaseTest.circle_case()
    CaseTest.single_fracture_case()

    Mesh2DTest.general_2d_test()
    Mesh2DTest.structured_quadrilateral_topology_test()
    Mesh2DTest.unstructured_triangle_topology_test()
