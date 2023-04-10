import sys
from typing import Any
import numpy as np
from .design_flow_base import DesignFlowBase
from mqhad.architecture_generator1.generator import Generator
from mqhad.mapper.mapper import Mapper
from mqhad.optimal_geometry_finder.optimal_geometry_finder import OptimalGeometryFinder
from mqhad.optimizer.optimizer import Optimizer
from qiskit import QuantumCircuit
from qiskit_metal import MetalGUI


class ConcreteDesignFlow1(DesignFlowBase):
    def __init__(
        self,
        circuit_path: str = "",
        config: dict = {},
        display_gui: bool = True,
        *args,
        **kwargs
    ):
        super().__init__(circuit_path=circuit_path, config=config)
        self._design_backend = "metal"
        self._display_gui = display_gui

    def read_circuit(self):
        self.qc = QuantumCircuit.from_qasm_file(self.circuit_path)

    def generate_architecture(self, qc: Any) -> tuple[np.ndarray, np.ndarray]:
        generator = Generator(qc=qc)
        qubit_grid, qubit_frequencies = generator.generate()
        return qubit_grid, qubit_frequencies

    def map_to_physical_layout(self, qubit_grid, qubit_frequencies):
        mapper = Mapper(
            design_backend=self._design_backend,
            qubit_grid=qubit_grid,
            qubit_frequencies=qubit_frequencies,
        )
        result = mapper.map()
        return result["canvas"]

    def load_optimal_geometry_finder(self, config: dict):
        return OptimalGeometryFinder(design_backend=self._design_backend, config=config)

    def optimize_layout(
        self, canvas, qubit_frequencies, config, optimal_geometry_finder
    ):
        optimizer = Optimizer(
            canvas=canvas,
            qubit_frequencies=qubit_frequencies,
            config=config,
            optimal_geometry_finder=optimal_geometry_finder,
        )
        optimizer.optimize()

    def display_gui(self):
        if self._display_gui == True:
            # We define a exit_no_operation() function that simply does nothing, and then use
            # the monkeypatch.setattr() method to replace the sys.exit() function with exit_noop() during the test.
            # This way, if the program calls sys.exit(), it will be replaced with the
            # no-op function and the test will continue to run instead of exiting.
            def exit_no_operation(status):
                pass

            gui = MetalGUI(self.canvas.get_canvas())
            q_app = gui.qApp
            print("Building GUI...")
            gui.rebuild()
            gui.autoscale()
            print("GUI built.")
            sys.exit = exit_no_operation
            sys.exit(q_app.exec_())
