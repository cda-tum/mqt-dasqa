import sys
from typing import Any
import numpy as np
from .design_flow_base import DesignFlowBase
from mqhad.architecture_generator1.generator import Generator
from mqhad.optimal_geometry_finder.optimal_geometry_finder import OptimalGeometryFinder
from mqhad.optimizer.optimizer import Optimizer
from qiskit import QuantumCircuit


class ConcreteDesignFlow1(DesignFlowBase):
    def __init__(
        self,
        circuit_path: str = "",
        config: dict = {},
        display_gui: bool = True,
        *args,
        **kwargs
    ):
        self._design_backend = "metal"
        self._display_gui = display_gui
        super().__init__(
            circuit_path=circuit_path,
            design_backend=self._design_backend,
            display_gui=self._display_gui,
            config=config,
        )

    def generate_architecture(
        self, qc: QuantumCircuit, config: dict
    ) -> tuple[np.ndarray, np.ndarray]:
        generator = Generator(qc=qc)
        qubit_grid, qubit_frequencies = generator.generate()
        return qubit_grid, qubit_frequencies

    def optimize_layout(self, canvas, qubit_frequencies, config):
        optimal_geometry_finder = OptimalGeometryFinder(
            design_backend=self._design_backend, config=config
        )
        optimizer = Optimizer(
            canvas=canvas,
            qubit_frequencies=qubit_frequencies,
            config=config,
            optimal_geometry_finder=optimal_geometry_finder,
        )
        optimizer.optimize()
