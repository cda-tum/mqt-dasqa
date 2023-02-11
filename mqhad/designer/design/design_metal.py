from .design_base import DesignBase
from qiskit_metal import designs


class DesignMetal(DesignBase):
    def __init__(self):
        pass

    def get_design(self):
        self._design = designs.DesignPlanar()
        return self._design
