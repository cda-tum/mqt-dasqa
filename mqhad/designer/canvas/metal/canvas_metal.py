from ..canvas_base import CanvasBase
from qiskit_metal import designs


class CanvasMetal(CanvasBase):
    def __init__(self):
        pass

    def get_canvas(self):
        self._canvas = designs.DesignPlanar()
        return self._canvas
