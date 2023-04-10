from abc import ABC, abstractmethod
from typing import Any, Union
import os
import numpy as np
from mqhad.mapper.canvas import CanvasBase
from mqhad.optimal_geometry_finder import OptimalGeometryFinderBase


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

    @abstractmethod
    def generate_architecture(self, qc: Any) -> tuple[np.ndarray, np.ndarray]:
        pass

    @abstractmethod
    def map_to_physical_layout(
        self, qubit_grid: np.ndarray, qubit_frequencies: np.ndarray
    ) -> CanvasBase:
        pass

    @abstractmethod
    def load_optimal_geometry_finder(self, config: dict):
        pass

    @abstractmethod
    def optimize_layout(
        self,
        canvas: CanvasBase,
        qubit_frequencies: np.ndarray,
        config: dict,
        optimal_geometry_finder: OptimalGeometryFinderBase,
    ):
        pass

    @abstractmethod
    def display_gui(self, canvas: CanvasBase):
        pass

    # Hooks
    def read_circuit(self):
        pass

    def run(self):
        if self._qc == None:
            self.read_circuit()

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

        print("#### Loading optimal geometry finder ####")
        self.optimal_geometry_finder = self.load_optimal_geometry_finder(self.config)
        print("#### Optimal geometry finder loaded ####")
        print("#### Optimizing design ####")
        self.optimize_layout(
            self.canvas,
            self.qubit_frequencies,
            self.config,
            self.optimal_geometry_finder,
        )
        print("#### Design optimized ####")

        self.display_gui(self.canvas)
