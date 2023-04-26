from ..canvas_base import CanvasBase
from qiskit_metal import designs


class Canvas(CanvasBase):
    def __init__(self):
        self._canvas = designs.DesignPlanar()

    def get_canvas(self):
        return self._canvas

    def update_component(self, component_name, option_name, option_value):
        self._canvas.components[component_name].options[option_name] = option_value
