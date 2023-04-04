from ..canvas_base import CanvasBase
from qiskit_metal import designs


class Canvas(CanvasBase):
    def __init__(self):
        self._canvas = designs.DesignPlanar()

    def get_canvas(self):
        return self._canvas
