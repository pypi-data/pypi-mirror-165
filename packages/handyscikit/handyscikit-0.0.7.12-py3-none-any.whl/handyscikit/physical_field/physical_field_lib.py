from .physical_field_base import PhysicalFieldBase
import numpy as np


class DarcyField(PhysicalFieldBase):
    def __init__(self, mesh):
        PhysicalFieldBase.__init__(self, mesh)

        self._cell_info = np.zeros([mesh.cell_num, 11], dtype=np.float32)  # axis 1 - (source, storage, permeability_matrix)
        self._name = "darcy"

        self._aquifer_thick = 1  # There is no influence on 3D, because its value is 1.

    def set_aquifer_thick(self, value):
        assert mesh.dim==2, "Darcy field in 3D doesn't have aquifer thick parameter."

        self._aquifer_thick = value

    @property
    def aquifer_thick(self):
        return self._aquifer_thick


class AbstractField(PhysicalFieldBase):
    def __init__(self, mesh):
        PhysicalFieldBase.__init__(self, mesh)

        self._cell_info = np.zeros([mesh.cell_num, 1], dtype=np.float32)
        self._name = "empty"