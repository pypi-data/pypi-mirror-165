from ..common.print_related import cprint


class DataFilter:
    @staticmethod
    def extract_horizontal_line_data(mesh, y, error=1e-6):
        """
        Extrace a horizontal line data.
        Rule is when a cell's y coordinate equals to y, then add this cell index to result.
        :param mesh: <MeshBase> Filtered mesh.
        :param y: <float> Chosen line coordinate.
        :param error: <float> Float equal error.
        :return: <list> Cell index list.
        """
        result = []

        for i in range(mesh.cell_num):
            if abs(mesh.cell_center[i, 1] - y) < error:
                result.append(i)

        try:
            assert len(result) != 0
        except:
            cprint("[handyscikit | DataFilter] There isn't a cell lies on this line in given mesh.")
            exit(1)

        return result

    @staticmethod
    def extract_vertical_line_data(mesh, x, error=1e-6):
        """
        Extract a vertical line data.
        Rule is when a cell's x coordinate equals to x, then add this cell index to result.
        :param mesh: <MeshBase> Filtered mesh.
        :param x: <float> Chosen line coordinate.
        :param error: <float> Float equal error.
        :return: <list> Cell index list.
        """
        result = []

        for i in range(mesh.cell_num):
            if abs(mesh.cell_center[i, 0] - x) < error:
                result.append(i)

        try:
            assert len(result) != 0
        except:
            cprint("[handyscikit | DataFilter] There isn't a cell lies on this line in given mesh.")
            exit(1)

        return result
