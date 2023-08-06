from .physical_field_base import PhysicalFieldBase
import gmsh
import numpy as np


class AbstractField(PhysicalFieldBase):
    def __init__(self, mesh):
        PhysicalFieldBase.__init__(self, mesh)

        self._cell_info = np.zeros([mesh.cell_num, 1], dtype=np.float32)
        self._name = "empty"


class ConvectionDiffusionField(PhysicalFieldBase):
    def __init__(self, mesh):
        PhysicalFieldBase.__init__(self, mesh)

        # axis 1 - (source, diffusion coefficient)
        self._cell_info = np.zeros([mesh.cell_num, 10], dtype=np.float32)
        self._name = "convection_diffusion"

        self._velocity = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    def set_physical_properties(self, areas, diffusion_coefficient):
        physical_group_dim_tag = (self._mesh.dim, gmsh.model.add_physical_group(self._mesh.dim, areas))
        self._physical_group_info[physical_group_dim_tag] = []
        self._physical_group_info[physical_group_dim_tag].append(diffusion_coefficient)
        self._physical_group_info[physical_group_dim_tag].append(diffusion_coefficient.flatten())

    def set_velocity(self, velocity):
        self._velocity = velocity


class DarcyField(PhysicalFieldBase):
    def __init__(self, mesh):
        PhysicalFieldBase.__init__(self, mesh)

        # axis 1 - (source, storage, permeability_matrix)
        self._cell_info = np.zeros([mesh.cell_num, 11], dtype=np.float32)
        self._name = "darcy"

        self._aquifer_thick = 1  # There is no influence on 3D, because its value is 1.

    def set_aquifer_thick(self, value):
        assert mesh.dim==2, "Darcy field in 3D doesn't have aquifer thick parameter."

        self._aquifer_thick = value

    def set_physical_properties(self, areas, storage, permeability):
        physical_group_dim_tag = (self._mesh.dim, gmsh.model.add_physical_group(self._mesh.dim, areas))
        self._physical_group_info[physical_group_dim_tag] = []
        self._physical_group_info[physical_group_dim_tag].append(storage)
        self._physical_group_info[physical_group_dim_tag].append(permeability)
        self._physical_group_info[physical_group_dim_tag].append(np.array([storage]+list(permeability.flatten())))

    @property
    def aquifer_thick(self):
        return self._aquifer_thick
