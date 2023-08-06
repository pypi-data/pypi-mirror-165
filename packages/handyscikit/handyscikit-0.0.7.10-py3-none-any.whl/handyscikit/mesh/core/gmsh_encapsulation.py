import gmsh

class GmshEncapsulation:
    class geom:
        @staticmethod
        def add_point(x, y, z, mesh_size=0, tag=-1):
            return gmsh.model.occ.add_point(x, y, z, meshSize=mesh_size, tag=tag)

        @staticmethod
        def add_rectangle(x, y, z, dx, dy, tag=-1, round_radius=0):
            return gmsh.model.occ.add_rectangle(x, y, z, dx, dy, tag=tag, roundedRadius=round_radius)

        @staticmethod
        def fragment(object_dim_tags, tool_dim_tags):
            gmsh.model.occ.fragment(object_dim_tags, tool_dim_tags, removeObject=True, removeTool=True)

        @staticmethod
        def synchronize(show_geom=False):
            gmsh.model.occ.synchronize()
            if show_geom: gmsh.fltk.run()

    class mesh:
        @staticmethod
        def recombine():
            gmsh.model.mesh.recombine()

        @staticmethod
        def set_size(dim_tags, size):
            gmsh.model.mesh.set_size(dim_tags, size)
