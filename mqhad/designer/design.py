import sys
from mqhad.designer.design_base import DesignBase
from mqhad.designer.canvas.metal import CanvasMetal
from mqhad.designer.qubit.metal import TransmonPocket6Qubit
from qiskit_metal import MetalGUI
import numpy as np


class Design(DesignBase):
    def __init__(
        self,
        design_backend: str = "metal",
        qubit_grid: np.ndarray = np.array([]),
        qubit_frequencies: np.ndarray = np.array([]),
    ):
        self._design_backend = design_backend
        self._qubit_grid = qubit_grid
        self._qubit_frequencies = qubit_frequencies

    def design(self):
        if self._design_backend == "metal":
            self._design_metal()

    def _design_metal(self):
        design = CanvasMetal().get_canvas()
        qubit = TransmonPocket6Qubit(design, self._qubit_grid).generate_qubit_layout()
        gui = MetalGUI(design)
        q_app = gui.qApp
        gui.rebuild()
        gui.autoscale()
        sys.exit(q_app.exec_())
