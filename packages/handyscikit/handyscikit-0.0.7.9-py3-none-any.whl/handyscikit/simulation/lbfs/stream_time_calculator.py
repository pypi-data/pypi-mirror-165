import numpy as np


class StreamTimeCalculator:
    @staticmethod
    def general_mesh(mesh):
        stream_time = np.zeros([mesh.face_num], dtype=np.float32)

        for i in range(mesh.face_num):
            radius = 0.0
            radius_initial_value = 0.0
            neighbor_cell_num_per_face = 2
            ghost_cell_index = -1

            # Loop two face neighbor cells.
            # There must be two cells in faces' neighbor.
            for j in range(neighbor_cell_num_per_face):
                cell_index = mesh.face_cell[i, j]
                if cell_index != ghost_cell_index:
                    # Loop cells' face.
                    for k in range(mesh.face_per_cell):
                        face_index = mesh.cell_face[cell_index, k]
                        # If this face is the calculating face, pass.
                        if face_index != i:
                            distance = point_to_line_distance(mesh.face_center[i],
                                                              mesh.nodes[mesh.faces[face_index, 0]],
                                                              mesh.nodes[mesh.faces[face_index, 1]])
                            if distance < radius or radius == radius_initial_value:
                                radius = distance

            stream_time[i] = radius / (2 ** 0.5)

        return stream_time

    @staticmethod
    def square_mesh(mesh):
        stream_time = np.zeros([mesh.face_num], dtype=np.float32)

        for i in range(mesh.face_num):
            neighbor_cell_num_per_face = 2
            ghost_cell_index = -1

            stream_time[i] = mesh.face_area[i]/2

        return stream_time

    @staticmethod
    def triangle_mesh(mesh):
        stream_time = np.zeros([mesh.face_num], dtype=np.float32)

        for i in range(mesh.face_num):
            radius = 0.0
            radius_initial_value = 0.0
            neighbor_cell_num_per_face = 2
            ghost_cell_index = -1

            # Loop two face neighbor cells.
            # There must be two cells in faces' neighbor.
            for j in range(neighbor_cell_num_per_face):
                cell_index = mesh.face_cell[i, j]
                if cell_index != ghost_cell_index:
                    # Loop cells' face.
                    for k in range(mesh.face_per_cell):
                        face_index = mesh.cell_face[cell_index, k]
                        # If this face is the calculating face, pass.
                        if face_index != i:
                            distance = mesh.cell_volume[cell_index] / mesh.face_area[face_index]
                            if distance < radius or radius == radius_initial_value:
                                radius = distance

            stream_time[i] = radius / (2 ** 0.5)

        return stream_time


def point_to_line_distance(point, face_point_0, face_point_1):
    face_length = np.linalg.norm(face_point_0 - face_point_1)

    vector_0 = point - face_point_0
    vector_1 = point - face_point_1

    return np.linalg.norm(np.cross(vector_0, vector_1)) / face_length
