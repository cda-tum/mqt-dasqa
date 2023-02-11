from mqhad.designer.canvas.metal import CanvasMetal
from qiskit_metal.designs import DesignPlanar


class TestCanvasMetal:
    def test_get_canvas(self):
        design_metal = CanvasMetal()
        design = design_metal.get_canvas()
        assert isinstance(design, DesignPlanar)
