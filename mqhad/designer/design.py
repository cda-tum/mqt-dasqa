import sys
from mqhad.designer.design_base import DesignBase
from mqhad.designer.canvas.metal import Canvas as MetalCanvas
from mqhad.designer.qubit.metal import TransmonPocket6Qubit as MetalTransmonPocket6Qubit
from mqhad.designer.qubit_connector.metal import (
    RouteMeanderConnector as MetalRouteMeanderConnector,
)
from mqhad.designer.launchpad.metal import Launchpad as MetalLaunchpad
from mqhad.designer.capacitor.metal import Capacitor as MetalCapacitor
from mqhad.designer.qubit_capacitor_connector.metal import QubitCapacitorConnector
from qiskit_metal import MetalGUI
import numpy as np


class Design(DesignBase):
    def __init__(
        self,
        design_backend: str = "metal",
        qubit_grid: np.ndarray = np.array([]),
        qubit_frequencies: np.ndarray = np.array([]),
        display_gui: bool = False,
    ):
        self._design_backend = design_backend
        self._qubit_grid = qubit_grid
        self._qubit_frequencies = qubit_frequencies
        self._display_gui = display_gui

    def design(self):
        if self._design_backend == "metal":
            self._design_metal(display_gui=self._display_gui)

    def _design_metal(self, display_gui: bool = False):
        print("Initializing Metal Canvas...")
        design = MetalCanvas().get_canvas()

        print("Generating qubits...")
        qubits = MetalTransmonPocket6Qubit(
            design, self._qubit_grid
        ).generate_qubit_layout()

        print("Generating qubit connections...")
        qubit_connections = MetalRouteMeanderConnector(
            design, self._qubit_grid, self._qubit_frequencies
        ).generate_qubit_connection()

        print("Generating launchpads...")
        launchpads = MetalLaunchpad(design, self._qubit_grid).generate_launchpad()

        print("Generating capacitors...")
        capacitors = MetalCapacitor(design, self._qubit_grid).generate_capacitor()

        print("Generating qubit-capacitor connections...")
        qubit_capacitor_connections = QubitCapacitorConnector(
            design, self._qubit_grid
        ).generate_qubit_capacitor_connection()

        if display_gui == True:
            # We define a exit_no_operation() function that simply does nothing, and then use
            # the monkeypatch.setattr() method to replace the sys.exit() function with exit_noop() during the test.
            # This way, if the program calls sys.exit(), it will be replaced with the
            # no-op function and the test will continue to run instead of exiting.
            def exit_no_operation(status):
                pass

            gui = MetalGUI(design)
            q_app = gui.qApp
            gui.rebuild()
            gui.autoscale()
            sys.exit = exit_no_operation
            sys.exit(q_app.exec_())
