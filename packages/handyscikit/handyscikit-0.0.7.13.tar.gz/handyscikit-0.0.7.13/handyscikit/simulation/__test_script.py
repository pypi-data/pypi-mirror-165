from handyscikit import cprint
from handyscikit.simulation import DataFilter, DataTransfer
from handyscikit.mesh import SquareCase
import numpy as np


class DataFileterTest:
    @staticmethod
    def extract_vertical_line_data_test():
        mesh = SquareCase(1)
        mesh.generate_structured([3, 3], show_mesh=False)
        mesh.clear_gmsh()

        get_index = DataFilter.extract_vertical_line_data(mesh, 0.5)

        assert get_index[0] == 3
        assert get_index[1] == 4
        assert get_index[2] == 5

        cprint("[ExtractVerticalLineData Test] Test passed.", color="green")

    @staticmethod
    def extrace_horizontal_line_data_test():
        mesh = SquareCase(1)
        mesh.generate_structured([3, 3], show_mesh=False)
        mesh.clear_gmsh()

        get_index = DataFilter.extract_horizontal_line_data(mesh, 0.5)

        assert get_index[0] == 1
        assert get_index[1] == 4
        assert get_index[2] == 7

        cprint("[ExtractVerticalLineData Test] Test passed.", color="green")


class DataTransferTest:
    @staticmethod
    def cell_to_node_test():
        mesh = SquareCase(1)
        mesh.generate_structured([2, 2], show_mesh=False)

        result = np.array([0, 1, 2, 3], dtype=np.float64)
        gradient = np.array([[1, 1, 0], [2, 2, 0], [3, 3, 0], [4, 4, 0]])
        node_data = DataTransfer.cell_to_node(mesh, result, gradient)

        assert node_data[0]==-0.5
        assert node_data[1]==2.0
        assert node_data[2]==5.0
        assert node_data[3]==1.0
        assert node_data[4]==0.25
        assert node_data[5]==3.25
        assert node_data[6]==2.5
        assert node_data[7]==0.0
        assert node_data[8]==1.125

        cprint("[DataTransferCellToNode Test] Test passed.", color="green")


if __name__ == "__main__":
    DataFileterTest.extract_vertical_line_data_test()
    DataFileterTest.extrace_horizontal_line_data_test()

    DataTransferTest.cell_to_node_test()