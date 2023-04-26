import sys
from typing import Any
from src.mapper.mapper_base import MapperBase
from src.mapper.canvas.metal import Canvas as MetalCanvas
from src.mapper.qubit.metal import TransmonPocket6Qubit as MetalTransmonPocket6Qubit
from src.mapper.qubit_connector.metal import (
    RouteMeanderConnector as MetalRouteMeanderConnector,
)
from src.mapper.launchpad.metal import Launchpad as MetalLaunchpad
from src.mapper.capacitor.metal import Capacitor as MetalCapacitor
from src.mapper.qubit_capacitor_connector.metal import (
    QubitCapacitorConnector as MetalQubitCapacitorConnector,
)
from src.mapper.capacitor_launchpad_connector.metal import (
    CapacitorLaunchpadConnector as MetalCapacitorLaunchpadConnector,
)
import numpy as np


class Mapper(MapperBase):
    def __init__(
        self,
        design_backend: str = "metal",
        qubit_grid: np.ndarray = np.array([]),
        qubit_frequencies: np.ndarray = np.array([]),
    ):
        self._design_backend = design_backend
        self._qubit_grid = qubit_grid[::-1]
        self._qubit_frequencies = qubit_frequencies

    def map(self):
        if self._design_backend == "metal":
            return self._map_metal()

    def _map_metal(self) -> Any:
        print("Initializing Metal Canvas...")
        canvas = MetalCanvas()
        design = canvas.get_canvas()

        result = {}

        print("Generating qubits...")
        result["qubits"] = MetalTransmonPocket6Qubit(
            design, self._qubit_grid
        ).generate_qubit_layout()

        print("Generating qubit connections...")
        result["qubit_connections"] = MetalRouteMeanderConnector(
            design, self._qubit_grid, self._qubit_frequencies
        ).generate_qubit_connection()

        print("Generating launchpads...")
        result["launchpads"] = MetalLaunchpad(
            design, self._qubit_grid
        ).generate_launchpad()

        print("Generating capacitors...")
        result["capacitors"] = MetalCapacitor(
            design, self._qubit_grid
        ).generate_capacitor()

        print("Generating qubit-capacitor connections...")
        result["qubit_capacitor_connections"] = MetalQubitCapacitorConnector(
            design, self._qubit_grid
        ).generate_qubit_capacitor_connection()

        print("Generating capacitor-launchpad connections...")
        result["capacitor_launchpad_connections"] = MetalCapacitorLaunchpadConnector(
            design, self._qubit_grid
        ).generate_capacitor_launchpad_connection()

        result["canvas"] = canvas

        return result
