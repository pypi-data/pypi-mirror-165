import vtkmodules.all as vtk


class VtkVisualizeBase:
    def __init__(self):
        # Actor property.
        self._actor_prop_geom = vtk.vtkProperty()
        self._actor_prop_geom.SetColor((0.91, 0.87, 0.67))
        self._actor_prop_geom.SetOpacity(0.3)
        self._actor_prop_geom.SetDiffuse(0)
        self._actor_prop_geom.SetAmbient(1)
        self._actor_prop_geom.SetLineWidth(1)
        self._actor_prop_mesh = vtk.vtkProperty()
        self._actor_prop_mesh.SetColor((0, 0, 0))
        self._actor_prop_mesh.SetOpacity(1)
        self._actor_prop_mesh.SetDiffuse(0)
        self._actor_prop_mesh.SetAmbient(1)
        self._actor_prop_mesh.SetLineWidth(1)
        # Color table.
        self._color_table = vtk.vtkLookupTable()
        self._color_table.SetRange(0, 1)
        self._color_table.SetHueRange(0.6804, 0)
        self._color_table.SetNumberOfColors(100)
        # Interactor.
        self._interactor = vtk.vtkRenderWindowInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        # Render window.
        self._render_window = vtk.vtkRenderWindow()
        self._render_window.SetSize(800, 800)
        # Interactor.
        self._interactor.SetRenderWindow(self._render_window)
        # Renderer.
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground((1, 1, 1))
        self._render_window.AddRenderer(self._renderer)
        # Scalarbar actor.
        self._scalarBarActor = vtk.vtkScalarBarActor()
        self._scalarBarActor.UnconstrainedFontSizeOn()
        self._scalarBarActor.GetLabelTextProperty().SetColor(0, 0, 0)
        self._scalarBarActor.GetLabelTextProperty().SetColor(124 / 255, 124 / 255, 124 / 255)
        self._scalarBarActor.GetLabelTextProperty().SetFontSize(13)
        self._scalarBarActor.GetLabelTextProperty().SetBold(False)
        self._scalarBarActor.GetLabelTextProperty().SetShadow(False)
        self._scalarBarActor.SetTitle("")
        self._scalarBarActor.SetWidth(0.05)
        self._scalarBarActor.SetHeight(0.6)
        self._scalarBarActor.SetNumberOfLabels(8)
        self._scalarBarActor.SetOrientationToVertical()
        self._scalarBarActor.GetPositionCoordinate().SetValue(0.9, 0.2)
        # Unstructured grid.
        # todo: uGrid directly use, uGrid reader need to use GetOutputPort().
        self._uGrid = None
        self._uGrid_reader = None
        self._uGrid_scalar_range = (0, 1)


class VtkVisualize(VtkVisualizeBase):
    def __init__(self):
        VtkVisualizeBase.__init__(self)

    def load_uGrid_data(self, mesh, result=None):
        # Make topology points.
        points = vtk.vtkPoints()
        points.Allocate(mesh.node_num)
        # todo: 2D case, is not 3D case.
        for node in mesh.nodes:
            points.InsertNextPoint(node[0], node[1], 0)

        # Make unstructured grid.
        self._uGrid = vtk.vtkUnstructuredGrid()
        self._uGrid.Allocate(mesh.cell_num)
        self._uGrid.SetPoints(points)
        for cell in mesh.cells:
            # todo: This type is only for polygon-4.
            self._uGrid.InsertNextCell(9, 4, (cell[0], cell[1], cell[2], cell[3]))

        # Scalars.
        if result is not None:
            # Make scalars.
            scalars = vtk.vtkDoubleArray()
            for num in result:
                scalars.InsertNextTuple1(num)
            self._uGrid.GetPointData().SetScalars(scalars)

            # Set look up table range.
            self._uGrid_scalar_range = (result.min(), result.max())
            self._color_table.SetRange(self._uGrid_scalar_range[0], self._uGrid_scalar_range[1])


    def load_uGrid_file(self, filename):
        # Make unstructured grid.
        self._uGrid_reader = vtk.vtkUnstructuredGridReader()
        self._uGrid_reader.SetFileName(filename)
        self._uGrid_reader.Update()

    def set_geometry_property(self, color, opacity=1, diffuse=0, ambient=1, line_width=1):
        """
        Change geometry actor porperty.
        :param color: Tuple | (R, G, B).
        :param opacity: Float | [0, 1] | 0 is transparent and 1 is solid.
        :param diffuse: Float | [0, 1]
        :param ambient: Float | [0, 1]
        :param line_width: Float
        :return:
        """
        self._actor_prop_geom.SetColor(color)
        self._actor_prop_geom.SetOpacity(opacity)
        self._actor_prop_geom.SetDiffuse(diffuse)
        self._actor_prop_geom.SetAmbient(ambient)
        self._actor_prop_geom.SetLineWidth(line_width)

    def set_mesh_property(self, color, opacity=1, diffuse=0, ambient=1, line_width=1):
        """
        Change mesh actor porperty.
        :param color: Tuple | (R, G, B) | (0, 0, 0) is black and (1, 1, 1) is white.
        :param opacity: Float | [0, 1] | 0 is transparent and 1 is solid.
        :param diffuse: Float | [0, 1]
        :param ambient: Float | [0, 1]
        :param line_width: Float
        :return:
        """
        self._actor_prop_mesh.SetColor(color)
        self._actor_prop_mesh.SetOpacity(opacity)
        self._actor_prop_mesh.SetDiffuse(diffuse)
        self._actor_prop_mesh.SetAmbient(ambient)
        self._actor_prop_mesh.SetLineWidth(line_width)

    def show_mesh(self):
        # Make geometry filter.
        geometryFileter = vtk.vtkGeometryFilter()
        geometryFileter.SetInputConnection(self._uGrid_reader.GetOutputPort())
        # Make polydata mapper.
        geometryMapper = vtk.vtkPolyDataMapper()
        geometryMapper.SetInputConnection(geometryFileter.GetOutputPort())
        # Extract edge.
        edges = vtk.vtkExtractEdges()
        edges.SetInputConnection(geometryFileter.GetOutputPort())
        # Edge mapper.
        edgeMapper = vtk.vtkPolyDataMapper()
        edgeMapper.SetInputConnection(edges.GetOutputPort())
        # Make geometry actor.
        geometry_actor = vtk.vtkActor()
        geometry_actor.SetMapper(geometryMapper)
        geometry_actor.SetProperty(self._actor_prop_geom)
        self._renderer.AddActor(geometry_actor)
        # Make edges actor.
        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edgeMapper)
        edge_actor.SetProperty(self._actor_prop_mesh)
        self._renderer.AddActor(edge_actor)
        # Show render window and start interact.
        self._interactor.Start()

    def show_contour(self, mesh=False):
        """

        :param mesh:
        :param result: Note that this result must be node value.
        :return:
        """
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(self._uGrid)
        mapper.SetScalarRange(self._uGrid_scalar_range[0], self._uGrid_scalar_range[1])
        mapper.SetLookupTable(self._color_table)
        # Make contour actor.
        contour_actor = vtk.vtkActor()
        contour_actor.SetMapper(mapper)
        if mesh:
            contour_actor.GetProperty().EdgeVisibilityOn()
        else:
            contour_actor.GetProperty().EdgeVisibilityOff()
        self._renderer.AddActor(contour_actor)
        # Make scalar bar.
        self._scalarBarActor.SetLookupTable(mapper.GetLookupTable())
        self._renderer.AddActor(self._scalarBarActor)
        # Show render window and start interact.
        self._interactor.Start()


"""Store for make coordinates for visualize actor."""
# axes = vtk.vtkCubeAxesActor()
# axes.SetZAxisVisibility(False) if self._dim == 2 else None
# axes.SetZAxisLabelVisibility(False) if self._dim == 2 else None
# axes.SetZAxisTickVisibility(False) if self._dim == 2 else None
# axes.SetZAxisMinorTickVisibility(False) if self._dim == 2 else None
# axes.SetScreenSize(self._text_size)
# axes.SetFlyModeToStaticEdges() if self._dim ==3 else axes.SetFlyModeToOuterEdges()
# ##
# axes.GetTitleTextProperty(0).SetColor(self._text_color)
# axes.GetTitleTextProperty(1).SetColor(self._text_color)
# axes.GetTitleTextProperty(2).SetColor(self._text_color) if self._dim == 3 else None
# axes.GetLabelTextProperty(0).SetColor(self._text_color)
# axes.GetLabelTextProperty(1).SetColor(self._text_color)
# axes.GetLabelTextProperty(2).SetColor(self._text_color) if self._dim == 3 else None
# axes.GetXAxesLinesProperty().SetColor(self._text_color)
# axes.GetYAxesLinesProperty().SetColor(self._text_color)
# axes.GetZAxesLinesProperty().SetColor(self._text_color) if self._dim == 3 else None
# axes.SetXTitle("X"), axes.SetYTitle("Y"), axes.SetZTitle("Z") if self._dim == 3 else None
# axes.SetXUnits("m"), axes.SetYUnits("m"), axes.SetZUnits("m") if self._dim == 3 else None
# ##
# xmin, xmax, ymin, ymax, zmin, zmax = main_actor.GetBounds()
# delta = min((xmax-xmin)*0.05, (ymax-ymin)*0.05, (zmax-zmin)*0.05) if self._dim==3 else min((xmax-xmin)*0.05, (ymax-ymin)*0.05)
# axes.SetBounds(xmin-delta, xmax+delta, ymin-delta, ymax+delta, zmin-delta, zmax+delta)
# axes.SetCamera(self._renderer.GetActiveCamera())
# self._renderer.AddActor(axes)

"""Store for write vtk file."""
# class VtkDatafileWriter():
#     def __init__(self, filename="test.vtk"):
#         self._file = open(filename, "w")
#         self._define_attributes()
#
#     def _define_attributes(self):
#         self._node = None               # 表征几何的节点坐标
#         self._cell = None               # 表征单元的拓扑关系数组
#         self._dim = None                # 数据集的维度
#         self._shape = None              # todo: 这里应该换成vertices_per_cell
#         self._node_num = None           # 几何的节点总数
#         self._cell_num = None           # 几何的单元总数
#         self._scalar = None             # 是否生成标量数据值
#         self._reload_flag = False       # 是否装载数据
#
#     def reload_data(self, node, cell, scalar=None):
#         """
#         生成vtk可视化文件 | Generate vtk visualization data file.
#         :param nodes: 网格节点数据（ndarray、n*dim）
#         :param cells: 网格单元数据（type、n*shape）
#         :param filename: 文件名
#         """
#         self._reload_flag = True
#         self._node = node
#         self._cell = cell
#         self._node_num = len(node)
#         self._dim = len(node[0])
#         self._cell_num = len(cell)
#         self._shape = len(cell[0])
#         self._scalar = scalar if scalar is not None else None
#         self._write_file_head()
#
#     def write_mesh_file(self):
#         self._write_node_data()
#         self._write_cell_data()
#         self._write_cell_type()
#         self._file.close()
#
#     def write_contour_file(self):
#         self._write_node_data()
#         self._write_cell_data()
#         self._write_cell_type()
#         self._write_node_scalar_data()
#         self._file.close()
#
#     def _write_file_head(self):
#         """
#         order --> data file version | file description | encoding type | dataset type
#         vtk DataFile Version 3.0
#         2D mesh data
#         ASCII
#         DATASET UNSTRUCTURED_GRID
#         """
#         self._file.write("# vtk DataFile Version 3.0\n%dD mesh data\nASCII\nDATASET UNSTRUCTURED_GRID" % self._dim)
#
#     def _write_node_data(self):
#         self._file.write("\nPOINTS %d float" % self._node_num + "\n")
#
#         if self._dim == 2:
#             for i in range(self._node_num):
#                 self._file.write(str(self._node[i][0])+" ")
#                 self._file.write(str(self._node[i][1])+" ")
#                 self._file.write("0\n")
#         elif self._dim == 3:
#             for i in range(self._node_num):
#                 self._file.write(str(self._node[i][0]) + " ")
#                 self._file.write(str(self._node[i][1]) + " ")
#                 self._file.write(str(self._node[i][2]) + "\n")
#
#     def _write_cell_data(self):
#         self._file.write("\nCELLS %d %d" % (self._cell_num, (self._shape + 1) * self._cell_num) + "\n")
#
#         for i in range(self._cell_num):
#             self._file.write(str(self._shape) + " ")
#             for j in range(self._shape):
#                 self._file.write(str(self._cell[i][j])+" ")
#             self._file.write("\n")
#
#     def _write_cell_type(self):
#         self._file.write("\nCELL_TYPES %d\n" % self._cell_num)
#         if self._shape == 3:  # 二维三角形面网格，三维三角形面网格
#             self._file.write("5 \n" * self._cell_num)
#         elif self._dim == 2 and self._shape == 4:  # 二维四边形网格
#             self._file.write("9 \n" * self._cell_num)
#         elif self._dim == 3 and self._shape == 4:  # 三维四面体网格
#             self._file.write("10 \n" * self._cell_num)
#         elif self._dim == 3 and self._shape == 8:  # 三维六面体网格
#             self._file.write("11 \n" * self._cell_num)
#         else:
#             error(False, "网格可视化文件尚无这种单元类型")
#
#     def _write_cell_scalar_data(self):
#         self._file.write("\nCELL_DATA %d\n" % self._cell_num)  # 单元数据
#         self._file.write("SCALARS fai float 1\n")               # 数据描述
#         self._file.write("LOOKUP_TABLE default\n")              # 颜色对照表
#
#         for i in range(self._cell_num):
#             self._file.write(str(self._scalar[i])+"\n")
#
#     def _write_node_scalar_data(self):
#         self._file.write("\nPOINT_DATA %d\n" % self._node_num)  # 单元数据
#         self._file.write("SCALARS fai float 1\n")               # 数据描述
#         self._file.write("LOOKUP_TABLE default\n")              # 颜色对照表
#
#         for i in range(self._node_num):
#             self._file.write(str(self._scalar[i])+"\n")

