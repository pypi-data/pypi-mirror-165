from handyscikit.plot import Figure
import numpy as np

"""Line plot"""
figure = Figure()
figure.set_title("3xn vs nx3 (mesh number 200)")
figure.set_x_label("案例")
figure.set_y_label("run time(s)")
base_data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
figure.set_base_data(base_data)
data_1 = np.array([0.124038, 0.12445, 0.122516, 0.120756, 0.122971, 0.122542, 0.122296, 0.122151, 0.12097, 0.122452])
figure.add_line_data(data_1, legend="data1")
data_2 = np.array([0.138069, 0.121229, 0.128158, 0.12646, 0.12979, 0.127898, 0.12959, 0.127754, 0.128288, 0.128105])
figure.add_line_data(data_2, legend="data2")
figure.set_y_limit([0.12, 0.14])
figure.add_legend()
# figure.show()
figure.save("1")

"""Line point plot"""
figure_1 = Figure()
base_data = np.array([0, 1, 2, 3, 4, 5])
figure_1.set_base_data(base_data)
figure_1.add_point_data(np.array([1, 2, 3, 4, 5, 6]))
figure_1.add_line_data(np.array([0, 3, 2, 1, 4, 5]))
figure_1.set_title("字体设置")
figure_1.set_x_label("x轴")
figure_1.set_y_label("y轴")
figure_1.set_y_limit([0, 6])
# figure_1.show()
figure.save("2")

"""Show vtk file mesh."""
from handyscikit.plot.vtk_visualize import VtkVisualize


visual = VtkVisualize()
visual.load_uGrid_file("airfoil3d.vtk")
visual.show_mesh()


"""Show contour from data."""
# from handyscikit.physics import mesh as meshTool
# import numpy as np
#
#
# mesh = meshTool.SquareMesh([1, 1], [2, 2])
# mesh.set_dirichlet_boundary(mesh.boundary_up, 1)
# mesh.set_dirichlet_boundary(mesh.boundary_down, 0)
# mesh.set_periodic_boundary([mesh.boundary_left, mesh.boundary_right])
#
# result = np.array([0, 1, 2, 3], dtype=np.float64)
# gradient = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float64)
# result_node = mesh.transfer_result_to_node_data(result, gradient)
#
# from handyscikit.plot import VtkVisualize
# visual = VtkVisualize()
# visual.load_uGrid_data(mesh, result_node)
# visual.show_contour()
