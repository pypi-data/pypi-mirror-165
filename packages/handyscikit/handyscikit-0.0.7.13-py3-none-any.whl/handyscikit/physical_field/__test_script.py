from handyscikit import cprint
from handyscikit.mesh import SquareCase
from handyscikit.analytical_solution import GaussianHill
from handyscikit.physical_field import DarcyField, AbstractField, PhysicalFields
import gmsh
import handyscikit as hsk
import numpy as np


class SingleField:
    class DirichletBoundary:
        @staticmethod
        def function_cos():
            mesh = SquareCase(1)
            mesh.generate_structured([3, 3])

            fields = PhysicalFields()

            empty_field = AbstractField(mesh)
            empty_field.set_boundary_as_dirichlet([mesh.boundary_up, mesh.boundary_down], "cos")
            empty_field.set_boundary_as_dirichlet([mesh.boundary_left, mesh.boundary_right], 9)
            fields.add_field(empty_field)

            fields.generate_info()

            assert empty_field.face_info[0, 0] == 1.0 and (empty_field.face_info[0, 1] - 0.5) < 1e-6
            assert empty_field.face_info[1, 0] == 1.0 and empty_field.face_info[1, 1] == -1.0
            assert empty_field.face_info[2, 0] == 1.0 and (empty_field.face_info[2, 1] - 0.5) < 1e-6
            assert empty_field.face_info[3, 0] == 1.0 and empty_field.face_info[3, 1] == 9.0
            assert empty_field.face_info[4, 0] == 1.0 and empty_field.face_info[4, 1] == 9.0
            assert empty_field.face_info[5, 0] == 1.0 and empty_field.face_info[5, 1] == 9.0
            assert empty_field.face_info[6, 0] == 1.0 and (empty_field.face_info[6, 1] - 0.5) < 1e-6
            assert empty_field.face_info[7, 0] == 1.0 and empty_field.face_info[7, 1] == -1.0
            assert empty_field.face_info[8, 0] == 1.0 and (empty_field.face_info[8, 1] - 0.5) < 1e-6
            assert empty_field.face_info[9, 0] == 1.0 and empty_field.face_info[9, 1] == 9.0
            assert empty_field.face_info[10, 0] == 1.0 and empty_field.face_info[10, 1] == 9.0
            assert empty_field.face_info[11, 0] == 1.0 and empty_field.face_info[11, 1] == 9.0
            assert empty_field.face_info[12, 0] == 0.0 and empty_field.face_info[12, 1] == 0.0
            assert empty_field.face_info[13, 0] == 0.0 and empty_field.face_info[13, 1] == 0.0
            assert empty_field.face_info[14, 0] == 0.0 and empty_field.face_info[14, 1] == 0.0
            assert empty_field.face_info[15, 0] == 0.0 and empty_field.face_info[15, 1] == 0.0
            assert empty_field.face_info[16, 0] == 0.0 and empty_field.face_info[16, 1] == 0.0
            assert empty_field.face_info[17, 0] == 0.0 and empty_field.face_info[17, 1] == 0.0
            assert empty_field.face_info[18, 0] == 0.0 and empty_field.face_info[18, 1] == 0.0
            assert empty_field.face_info[19, 0] == 0.0 and empty_field.face_info[19, 1] == 0.0
            assert empty_field.face_info[20, 0] == 0.0 and empty_field.face_info[20, 1] == 0.0
            assert empty_field.face_info[21, 0] == 0.0 and empty_field.face_info[21, 1] == 0.0
            assert empty_field.face_info[22, 0] == 0.0 and empty_field.face_info[22, 1] == 0.0
            assert empty_field.face_info[23, 0] == 0.0 and empty_field.face_info[23, 1] == 0.0

            cprint("[PhysicalFields Test] Dirichlet function cos boundary test passed.", color="green")

        @staticmethod
        def scalar():
            mesh = SquareCase(1)
            mesh.generate_structured([2, 2])

            fields = PhysicalFields()

            empty_field = AbstractField(mesh)
            empty_field.set_boundary_as_dirichlet([mesh.boundary_up], 1)
            empty_field.set_boundary_as_dirichlet([mesh.boundary_down], 2)
            empty_field.set_boundary_as_dirichlet([mesh.boundary_left], 3)
            empty_field.set_boundary_as_dirichlet([mesh.boundary_right], 4)
            fields.add_field(empty_field)

            fields.generate_info()

            assert empty_field.face_info[0, 0] == 1.0 and empty_field.face_info[0, 1] == 2.0
            assert empty_field.face_info[1, 0] == 1.0 and empty_field.face_info[1, 1] == 2.0
            assert empty_field.face_info[2, 0] == 1.0 and empty_field.face_info[2, 1] == 4.0
            assert empty_field.face_info[3, 0] == 1.0 and empty_field.face_info[3, 1] == 4.0
            assert empty_field.face_info[4, 0] == 1.0 and empty_field.face_info[4, 1] == 1.0
            assert empty_field.face_info[5, 0] == 1.0 and empty_field.face_info[5, 1] == 1.0
            assert empty_field.face_info[6, 0] == 1.0 and empty_field.face_info[6, 1] == 3.0
            assert empty_field.face_info[7, 0] == 1.0 and empty_field.face_info[7, 1] == 3.0
            assert empty_field.face_info[8, 0] == 0.0 and empty_field.face_info[8, 1] == 0.0
            assert empty_field.face_info[9, 0] == 0.0 and empty_field.face_info[9, 1] == 0.0
            assert empty_field.face_info[10, 0] == 0.0 and empty_field.face_info[10, 1] == 0.0
            assert empty_field.face_info[11, 0] == 0.0 and empty_field.face_info[11, 1] == 0.0

            cprint("[PhysicalFields Test] Dirichlet scalar boundary test passed.", color="green")

    class InitialCondition:
        @staticmethod
        def function():
            mesh = SquareCase(2, coordinate=[-1, -1])
            mesh.generate_structured([3, 3])

            fields = PhysicalFields()

            empty_field = AbstractField(mesh)
            gauss = GaussianHill(0.05, np.array([[0.001, 0], [0, 0.001]]))
            empty_field.set_initial_condition_by_func(gauss.calc_initial_condition)
            fields.add_field(empty_field)

            fields.generate_info()

            error = 1e-6
            assert empty_field.initial_condition[0] == 0.0
            assert abs(empty_field.initial_condition[1] - 2.489108e-39) < error
            assert empty_field.initial_condition[2] == 0.0
            assert abs(empty_field.initial_condition[3] - 2.489147e-39) < error
            assert empty_field.initial_condition[4] == 1.0
            assert abs(empty_field.initial_condition[5] - 2.489108e-39) < error
            assert empty_field.initial_condition[6] == 0.0
            assert abs(empty_field.initial_condition[7] - 2.489108e-39) < error
            assert empty_field.initial_condition[8] == 0.0

            cprint("[PhysicalFields Test] Initial condition function test passed.", color="green")

        @staticmethod
        def scalar():
            mesh = SquareCase(1)
            mesh.generate_structured([2, 2])

            fields = PhysicalFields()

            empty_field = AbstractField(mesh)
            empty_field.set_initial_condition_by_scalar(2.5)
            fields.add_field(empty_field)

            fields.generate_info()

            assert np.all(empty_field.initial_condition==2.5)

            cprint("[PhysicalFields Test] Initial condition scalar test passed.", color="green")

    class PeriodicBoundary:
        @staticmethod
        def basic():
            mesh = SquareCase(1)
            mesh.generate_structured([3, 3])

            fields = PhysicalFields()

            empty = AbstractField(mesh)
            empty.set_boundary_as_periodic([mesh.boundary_up, mesh.boundary_down])
            empty.set_boundary_as_periodic([mesh.boundary_left, mesh.boundary_right])
            fields.add_field(empty)

            fields.generate_info()

            assert empty.face_info[0, 0] == 4.0 and empty.face_info[0, 1] == 8.0 and empty.face_info[0, 2] == 2.0
            assert empty.face_info[1, 0] == 4.0 and empty.face_info[1, 1] == 7.0 and empty.face_info[1, 2] == 5.0
            assert empty.face_info[2, 0] == 4.0 and empty.face_info[2, 1] == 6.0 and empty.face_info[2, 2] == 8.0
            assert empty.face_info[3, 0] == 4.0 and empty.face_info[3, 1] == 11.0 and empty.face_info[3, 2] == 0.0
            assert empty.face_info[4, 0] == 4.0 and empty.face_info[4, 1] == 10.0 and empty.face_info[4, 2] == 1.0
            assert empty.face_info[5, 0] == 4.0 and empty.face_info[5, 1] == 9.0 and empty.face_info[5, 2] == 2.0
            assert empty.face_info[6, 0] == 4.0 and empty.face_info[6, 1] == 2.0 and empty.face_info[6, 2] == 6.0
            assert empty.face_info[7, 0] == 4.0 and empty.face_info[7, 1] == 1.0 and empty.face_info[7, 2] == 3.0
            assert empty.face_info[8, 0] == 4.0 and empty.face_info[8, 1] == 0.0 and empty.face_info[8, 2] == 0.0
            assert empty.face_info[9, 0] == 4.0 and empty.face_info[9, 1] == 5.0 and empty.face_info[9, 2] == 8.0
            assert empty.face_info[10, 0] == 4.0 and empty.face_info[10, 1] == 4.0 and empty.face_info[10, 2] == 7.0
            assert empty.face_info[11, 0] == 4.0 and empty.face_info[11, 1] == 3.0 and empty.face_info[11, 2] == 6.0
            assert empty.face_info[12, 0] == 0.0 and empty.face_info[12, 1] == 0.0 and empty.face_info[12, 2] == 0.0
            assert empty.face_info[13, 0] == 0.0 and empty.face_info[13, 1] == 0.0 and empty.face_info[13, 2] == 0.0
            assert empty.face_info[14, 0] == 0.0 and empty.face_info[14, 1] == 0.0 and empty.face_info[14, 2] == 0.0
            assert empty.face_info[15, 0] == 0.0 and empty.face_info[15, 1] == 0.0 and empty.face_info[15, 2] == 0.0
            assert empty.face_info[16, 0] == 0.0 and empty.face_info[16, 1] == 0.0 and empty.face_info[16, 2] == 0.0
            assert empty.face_info[17, 0] == 0.0 and empty.face_info[17, 1] == 0.0 and empty.face_info[17, 2] == 0.0
            assert empty.face_info[18, 0] == 0.0 and empty.face_info[18, 1] == 0.0 and empty.face_info[18, 2] == 0.0
            assert empty.face_info[19, 0] == 0.0 and empty.face_info[19, 1] == 0.0 and empty.face_info[19, 2] == 0.0
            assert empty.face_info[20, 0] == 0.0 and empty.face_info[20, 1] == 0.0 and empty.face_info[20, 2] == 0.0
            assert empty.face_info[21, 0] == 0.0 and empty.face_info[21, 1] == 0.0 and empty.face_info[21, 2] == 0.0
            assert empty.face_info[22, 0] == 0.0 and empty.face_info[22, 1] == 0.0 and empty.face_info[22, 2] == 0.0
            assert empty.face_info[23, 0] == 0.0 and empty.face_info[23, 1] == 0.0 and empty.face_info[23, 2] == 0.0

            cprint("[PhysicalFields Test] Periodic boundary test passed.", color="green")

    class PhysicalProperties:
        @staticmethod
        def basic():
            mesh = SquareCase(1)
            mesh.generate_structured([2, 2])

            fields = PhysicalFields()

            darcy_field = DarcyField(mesh)
            darcy_field.set_physical_properties([1], [1e-6, 4e-13, 0, 0, 0, 4e-13, 0, 0, 0, 4e-13])
            fields.add_field(darcy_field)

            fields.generate_info()

            error = 1e-6
            assert abs(darcy_field.cell_info[0, 1] - 1e-6) < error and abs(darcy_field.cell_info[0, 2] - 4e-13) < error
            assert abs(darcy_field.cell_info[1, 1] - 1e-6) < error and abs(darcy_field.cell_info[1, 2] - 4e-13) < error
            assert abs(darcy_field.cell_info[2, 1] - 1e-6) < error and abs(darcy_field.cell_info[2, 2] - 4e-13) < error
            assert abs(darcy_field.cell_info[3, 1] - 1e-6) < error and abs(darcy_field.cell_info[3, 2] - 4e-13) < error

            cprint("[PhysicalFields Test] Physical properties test passed.", color="green")

    class Source:
        @staticmethod
        def point():
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

            fields = PhysicalFields()

            empty_field = AbstractField(mesh)
            empty_field.set_point_source([6], 6)
            empty_field.set_point_source([5], 5)
            fields.add_field(empty_field)

            fields.generate_info()

            assert empty_field.cell_info[0, 0] == 1.0
            assert empty_field.cell_info[1, 0] == 1.0
            assert empty_field.cell_info[2, 0] == 1.0
            assert empty_field.cell_info[3, 0] == 1.0
            assert empty_field.cell_info[4, 0] == 0.0
            assert empty_field.cell_info[5, 0] == 0.0
            assert empty_field.cell_info[6, 0] == 0.0
            assert empty_field.cell_info[7, 0] == 0.0
            assert empty_field.cell_info[8, 0] == 2.0
            assert empty_field.cell_info[9, 0] == 2.0
            assert empty_field.cell_info[10, 0] == 1.0
            assert empty_field.cell_info[11, 0] == 1.0
            assert empty_field.cell_info[12, 0] == 0.0
            assert empty_field.cell_info[13, 0] == 1.0

            cprint("[PhysicalFields Test] Point source test passed.", color="green")


if __name__ == "__main__":
    SingleField.DirichletBoundary.function_cos()
    SingleField.DirichletBoundary.scalar()
    SingleField.InitialCondition.function()
    SingleField.InitialCondition.scalar()
    SingleField.PeriodicBoundary.basic()
    SingleField.PhysicalProperties.basic()
    SingleField.Source.point()
