from mqhad.designer.design import DesignMetal
from qiskit_metal.designs import DesignPlanar


class TestDesigner:
    def test_get_design(self):
        design_metal = DesignMetal()
        design = design_metal.get_design()
        assert isinstance(design, DesignPlanar)
