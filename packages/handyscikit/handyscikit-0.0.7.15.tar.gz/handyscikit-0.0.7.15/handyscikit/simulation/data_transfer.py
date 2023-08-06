from ..common.print_related import cprint
import numpy as np


class DataTransfer:
    @staticmethod
    def cell_to_node(mesh, result, gradient):
        """
        Change cell-centered result to node result.
        :param mesh:  <MeshBase> Transfer mesh.
        :param result: <float, ndarray> Cell center result.
        :param gradient: <float, ndarray> Cell center gradient.
        :return: <float, ndarray> Node value list.
        """
        cprint("[handyscikit | Mesh] Transfer cell data to node data.", color="purple")

        tmp = [[] for _ in range(mesh.node_num)]
        for i in range(mesh.cell_num):
            for j in mesh.cells[i]:
                tmp[j].append(result[i] + np.dot(mesh.nodes[j] - mesh.cell_center[i], gradient[i]))

        for i in range(mesh.node_num):
            tmp[i] = sum(tmp[i])/len(tmp[i])

        # Boundary correction.
        # todo: 2D corner condition.
        # todo: Low precision for variant Dirichlet boudnary.
        # todo: Pass periodic boundary condition.
        for i in range(mesh.face_num):
            if mesh.face_info[i, 0] == 1:
                tmp[mesh.faces[i, 0]] = mesh.face_info[i, 1]
                tmp[mesh.faces[i, 1]] = mesh.face_info[i, 1]

        return np.array(tmp, dtype=np.float64)
