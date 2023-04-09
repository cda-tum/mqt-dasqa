from abc import ABC, abstractmethod
from typing import Any
import os
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
        return self._qubit_grid

    @qubit_grid.setter
    def qubit_grid(self, qubit_grid: dict):
        self._qubit_grid = qubit_grid

    @property
    def qubit_frequencies(self):
        return self._qubit_frequencies

    @qubit_frequencies.setter
    def qubit_frequencies(self, qubit_frequencies: dict):
        self._qubit_frequencies = qubit_frequencies

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, canvas: CanvasBase):
        self._canvas = canvas

    @abstractmethod
    def generate_architecture(self):
        pass

    @abstractmethod
    def map_to_physical_layout(self):
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
        self.generate_architecture()
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
