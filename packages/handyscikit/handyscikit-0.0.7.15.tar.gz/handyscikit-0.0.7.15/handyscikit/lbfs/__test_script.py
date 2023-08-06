from handyscikit import cprint
from handyscikit.mesh import SquareCase
from handyscikit.lbfs import StreamTimeCalculator
import numpy as np


class StreamTimeCalculatorTest:
    @staticmethod
    def general_mesh():
        mesh = SquareCase(1)
        mesh.set_dirichlet_boundary([mesh.boundary_up], 1)
        mesh.set_dirichlet_boundary([mesh.boundary_down], 2)
        mesh.set_dirichlet_boundary([mesh.boundary_left], 3)
        mesh.set_dirichlet_boundary([mesh.boundary_right], 4)
        mesh.generate_unstructured([0.5, 0.5, 0.5, 0.5], show_mesh=False)

        error = 1e-6
        stream_time = StreamTimeCalculator.general_mesh(mesh)
        assert abs(stream_time[0] - 0.12382627) < error
        assert stream_time[1] == 0.125
        assert stream_time[2] == 0.125
        assert abs(stream_time[3] - 0.12500001) < error
        assert abs(stream_time[4] - 0.12500001) < error
        assert stream_time[5] == 0.125
        assert stream_time[6] == 0.125
        assert abs(stream_time[7] - 0.12616281) < error
        assert abs(stream_time[8] - 0.12404647) < error
        assert abs(stream_time[9] - 0.11306018) < error
        assert abs(stream_time[10] - 0.13258252) < error
        assert abs(stream_time[11] - 0.11336884) < error
        assert abs(stream_time[12] - 0.11628257) < error
        assert abs(stream_time[13] - 0.10924837) < error
        assert abs(stream_time[14] - 0.09943689) < error
        assert abs(stream_time[15] - 0.09943689) < error
        assert abs(stream_time[16] - 0.09943689) < error
        assert abs(stream_time[17] - 0.09241478) < error
        assert abs(stream_time[18] - 0.09241478) < error
        assert abs(stream_time[19] - 0.0924148) < error
        assert abs(stream_time[20] - 0.10966435) < error
        assert abs(stream_time[21] - 0.10925686) < error
        assert abs(stream_time[22] - 0.10481568) < error
        assert abs(stream_time[23] - 0.11228142) < error
        assert abs(stream_time[24] - 0.11293966) < error

        cprint("[StreamTimeCalculator Test] General mesh test passed.", color="green")

    @staticmethod
    def square_mesh():
        mesh = SquareCase(1)
        mesh.generate_structured([2, 2], show_mesh=False)

        stream_time = StreamTimeCalculator.square_mesh(mesh)
        assert np.all(stream_time==0.25)

        cprint("[StreamTimeCalculator Test] Square mesh test passed.", color="green")

    @staticmethod
    def triangle_mesh():
        mesh = SquareCase(1)
        mesh.set_dirichlet_boundary([mesh.boundary_up], 1)
        mesh.set_dirichlet_boundary([mesh.boundary_down], 2)
        mesh.set_dirichlet_boundary([mesh.boundary_left], 3)
        mesh.set_dirichlet_boundary([mesh.boundary_right], 4)
        mesh.generate_unstructured([0.5, 0.5, 0.5, 0.5], show_mesh=False)

        error = 1e-6
        stream_time = StreamTimeCalculator.triangle_mesh(mesh)
        assert abs(stream_time[0] - 0.12382627) < error
        assert stream_time[1] == 0.125
        assert stream_time[2] == 0.125
        assert abs(stream_time[3] - 0.12500001) < error
        assert abs(stream_time[4] - 0.12500001) < error
        assert stream_time[5] == 0.125
        assert stream_time[6] == 0.125
        assert abs(stream_time[7] - 0.12616281) < error
        assert abs(stream_time[8] - 0.12404647) < error
        assert abs(stream_time[9] - 0.11306018) < error
        assert abs(stream_time[10] - 0.13258252) < error
        assert abs(stream_time[11] - 0.11336884) < error
        assert abs(stream_time[12] - 0.11628257) < error
        assert abs(stream_time[13] - 0.10924837) < error
        assert abs(stream_time[14] - 0.09943689) < error
        assert abs(stream_time[15] - 0.09943689) < error
        assert abs(stream_time[16] - 0.09943689) < error
        assert abs(stream_time[17] - 0.09241478) < error
        assert abs(stream_time[18] - 0.09241478) < error
        assert abs(stream_time[19] - 0.0924148) < error
        assert abs(stream_time[20] - 0.10966435) < error
        assert abs(stream_time[21] - 0.10925686) < error
        assert abs(stream_time[22] - 0.10481568) < error
        assert abs(stream_time[23] - 0.11228142) < error
        assert abs(stream_time[24] - 0.11293966) < error

        cprint("[StreamTimeCalculator Test] Triangle mesh test passed.", color="green")


if __name__ == "__main__":
    StreamTimeCalculatorTest.general_mesh()
    StreamTimeCalculatorTest.square_mesh()
    StreamTimeCalculatorTest.triangle_mesh()
