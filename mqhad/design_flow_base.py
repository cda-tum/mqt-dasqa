from abc import ABC, abstractmethod
from typing import final, Any, Union
import sys
import os
import numpy as np
from mqhad.mapper.canvas import CanvasBase
from mqhad.mapper.mapper import Mapper
from mqhad.optimal_geometry_finder import OptimalGeometryFinderBase
from qiskit import QuantumCircuit
from qiskit_metal import MetalGUI


class DesignFlowBase(ABC):
    def __init__(
        self,
        circuit_path: str = "",
        design_backend: str = "metal",
        display_gui: bool = True,
        config: dict = {},
        *args,
        **kwargs
    ):
        self.config = config
        self.circuit_path = circuit_path
        self._design_backend = design_backend
        self._display_gui = display_gui

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: dict):
        self._config = config

    @property
    def qc(self):
        return self._qc

    @qc.setter
    def qc(self, qc: Any):
        self._qc = qc

    @property
    def circuit_path(self):
        return self._circuit_path

    @circuit_path.setter
    def circuit_path(self, circuit_path: str):
        if os.path.exists(circuit_path) == False:
            raise ValueError("Circuit path does not exist.")
        self._circuit_path = circuit_path

    @property
    def qubit_grid(self):
        if hasattr(self, "_qubit_grid") == False:
            raise ValueError("Qubit grid not generated.")
        return self._qubit_grid

    @qubit_grid.setter
    def qubit_grid(self, qubit_grid: Union[list[list], np.ndarray]):
        if isinstance(qubit_grid, np.ndarray) == False:
            qubit_grid = np.array(qubit_grid)
        if qubit_grid.ndim != 2:
            raise ValueError("Qubit grid must be a 2D array.")
        self._qubit_grid = qubit_grid

    @property
    def qubit_frequencies(self):
        if hasattr(self, "_qubit_frequencies") == False:
            raise ValueError("Qubit frequencies not generated.")
        return self._qubit_frequencies

    @qubit_frequencies.setter
    def qubit_frequencies(self, qubit_frequencies: np.ndarray):
        if isinstance(qubit_frequencies, np.ndarray) == False:
            qubit_frequencies = np.array(qubit_frequencies)
        if qubit_frequencies.ndim != 1:
            raise ValueError("Qubit frequencies must be a 1D array.")
        self._qubit_frequencies = qubit_frequencies

    @property
    def canvas(self):
        if hasattr(self, "_canvas") == False:
            raise ValueError("Physical layout not generated.")
        return self._canvas

    @canvas.setter
    def canvas(self, canvas: CanvasBase):
        if isinstance(canvas, CanvasBase) == False:
            raise ValueError("Canvas must be an instance of Canvas.")
        self._canvas = canvas

    @property
    def optimal_geometry_finder(self):
        if hasattr(self, "_optimal_geometry_finder") == False:
            raise ValueError("Optimal geometry finder not loaded.")
        return self._optimal_geometry_finder

    @optimal_geometry_finder.setter
    def optimal_geometry_finder(self, optimal_geometry_finder: Any):
        if isinstance(optimal_geometry_finder, OptimalGeometryFinderBase) == False:
            raise ValueError(
                "Optimal geometry finder must be an instance of OptimalGeometryFinderBase."
            )
        self._optimal_geometry_finder = optimal_geometry_finder

    @final
    def read_circuit(self, circuit_path: str):
        self.qc = QuantumCircuit.from_qasm_file(circuit_path)

    @final
    def map_to_physical_layout(
        self, qubit_grid: np.ndarray, qubit_frequencies: np.ndarray
    ) -> CanvasBase:
        mapper = Mapper(
            design_backend=self._design_backend,
            qubit_grid=qubit_grid,
            qubit_frequencies=qubit_frequencies,
        )
        result = mapper.map()
        return result["canvas"]

    @final
    def display_gui(self, canvas: CanvasBase):
        if self._display_gui == True:
            # We define a exit_no_operation() function that simply does nothing, and then use
            # the monkeypatch.setattr() method to replace the sys.exit() function with exit_noop() during the test.
            # This way, if the program calls sys.exit(), it will be replaced with the
            # no-op function and the test will continue to run instead of exiting.
            def exit_no_operation(status):
                pass

            gui = MetalGUI(canvas.get_canvas())
            q_app = gui.qApp
            print("Building GUI...")
            gui.rebuild()
            gui.autoscale()
            print("GUI built.")
            sys.exit = exit_no_operation
            sys.exit(q_app.exec_())

    @abstractmethod
    def generate_architecture(
        self, qc: QuantumCircuit
    ) -> tuple[np.ndarray, np.ndarray]:
        pass

    @abstractmethod
    def optimize_layout(
        self,
        canvas: CanvasBase,
        qubit_frequencies: np.ndarray,
        config: dict,
    ):
        pass

    def run(self):
        self.read_circuit(self.circuit_path)

        print("#### Start generating architecture ####")
        self.qubit_grid, self.qubit_frequencies = self.generate_architecture(self.qc)
        print("#### Architecture generated ####")
        print("Qubit grid:", self.qubit_grid)
        print("Qubit frequencies:", self.qubit_frequencies)

        print("#### Start mapping to physical layout ####")
        self.canvas = self.map_to_physical_layout(
            self.qubit_grid, self.qubit_frequencies
        )
        print("#### Physical layout generated ####")

        print("#### Optimizing design ####")
        self.optimize_layout(self.canvas, self.qubit_frequencies, self.config)
        print("#### Design optimized ####")

        self.display_gui(self.canvas)
