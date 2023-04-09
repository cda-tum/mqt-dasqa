from abc import ABC, abstractmethod
from typing import Any, Union
import os
import numpy as np
from mqhad.mapper.canvas import CanvasBase


class DesignFlowBase(ABC):
    def __init__(
        self, qc: Any = None, circuit_path: str = "", config: dict = {}, *args, **kwargs
    ):
        self.config = config
        self.qc = qc
        self.circuit_path = circuit_path

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
        self._canvas = canvas

    @abstractmethod
    def generate_architecture(self) -> tuple[np.ndarray, np.ndarray]:
        pass

    @abstractmethod
    def map_to_physical_layout(self) -> CanvasBase:
        pass

    @abstractmethod
    def optimize_design(self):
        pass

    @abstractmethod
    def display_gui(self):
        pass

    # Hooks
    def read_circuit(self):
        pass

    def run(self):
        if self._qc == None:
            self.read_circuit()

        print("#### Start generating architecture ####")
        self.qubit_grid, self.qubit_frequencies = self.generate_architecture()
        print("#### Architecture generated ####")
        print("Qubit grid:", self.qubit_grid)
        print("Qubit frequencies:", self.qubit_frequencies)

        print("#### Start mapping to physical layout ####")
        self.map_to_physical_layout()
        print("#### Physical layout generated ####")

        print("Optimizing design...")
        self.optimize_design()
        print("Design optimized")

        self.display_gui()
