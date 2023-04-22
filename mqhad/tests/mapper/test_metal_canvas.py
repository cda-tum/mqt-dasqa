from unittest.mock import MagicMock
from mqhad.mapper.canvas.metal import Canvas
from qiskit_metal.designs import DesignPlanar


class TestMetalCanvas:
    def test_get_canvas(self):
        design_metal = Canvas()
        design = design_metal.get_canvas()
        assert isinstance(design, DesignPlanar)

    def test_update_components(self):
        class CanvasMock(Canvas):
            def __init__(self):
                pass

        design_metal = CanvasMock()
        mock_design = MagicMock(name="mock_design")
        design_metal._canvas = mock_design

        design_metal.update_component("Q_0", "fQ", 5.3)

        assert mock_design.components.__getitem__().options.__setitem__.call_count == 1
