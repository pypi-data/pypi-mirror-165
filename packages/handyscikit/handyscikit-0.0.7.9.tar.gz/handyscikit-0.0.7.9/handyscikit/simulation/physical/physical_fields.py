import gmsh


class PhysicalFields:
    def __init__(self):
        self._fields = []
        self._time_invertal = None
        self._time_steps = None

    def add_field(self, field_object):
        self._fields.append(field_object)

    def get_field(self, field_name):
        for field in self._fields:
            if field.name == field_name:
                return field

    def generate_info(self):
        assert len(self._fields) != 0, "There is no field in physical fields."

        for field in self._fields:
            field.generate_info()

        gmsh.clear()

    def set_time(self, time_interval, time_steps):
        self._time_invertal = time_interval
        self._time_steps = time_steps

    @property
    def time_interval(self):
        return self._time_invertal

    @property
    def time_steps(self):
        return self._time_steps

