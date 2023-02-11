from mqhad.designer.canvas.metal import Canvas
from qiskit_metal.designs import DesignPlanar


class TestMetalCanvas:
    def test_get_canvas(self):
        design_metal = Canvas()
        design = design_metal.get_canvas()
        assert isinstance(design, DesignPlanar)
