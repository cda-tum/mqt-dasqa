import sys
from mqhad.designer.design_base import DesignBase
from mqhad.designer.canvas.metal import Canvas as MetalCanvas
from mqhad.designer.qubit.metal import TransmonPocket6Qubit as MetalTransmonPocket6Qubit
from mqhad.designer.qubit_connection.metal import (
    RouteMeanderConnector as MetalRouteMeanderConnector,
)
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
        design = MetalCanvas().get_canvas()
        qubit = MetalTransmonPocket6Qubit(
            design, self._qubit_grid
        ).generate_qubit_layout()
        qubit_connection = MetalRouteMeanderConnector(
            design, self._qubit_grid, self._qubit_frequencies
        ).generate_qubit_connection()
        gui = MetalGUI(design)
        q_app = gui.qApp
        gui.rebuild()
        gui.autoscale()
        sys.exit(q_app.exec_())
