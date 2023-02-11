from collections import OrderedDict
from .qubit_base import QubitBase
from qiskit_metal.designs import DesignPlanar
import numpy as np


class QubitMetal(QubitBase):
    def __init__(
        self, design: DesignPlanar = None, qubit_grid: np.ndarray = np.array([])
    ):
        self._design = design
        self._qubit_grid = qubit_grid

    def generate_qubit_layout(self):
        pass

    def _get_open_qubit_pins(self, qubit_grid: np.ndarray) -> dict[int,list[str]]:

        pins_to_remove = OrderedDict()
        N_x = len(qubit_grid[0])
        N_y = len(qubit_grid)
        #Loop to generate and draw the launchpads
        for x in range(N_x):
            for y in range(N_y):
                current_qubit = qubit_grid[y][x]
                if current_qubit == -1:
                    continue
                
                surrounding_qubits = {
                    "left": self._get_qubit(qubit_grid, y, x-1),
                    "right": self._get_qubit(qubit_grid, y, x+1),
                    "top": self._get_qubit(qubit_grid, y+1, x),
                    "bottom": self._get_qubit(qubit_grid, y-1, x),
                }
                pins_to_remove[current_qubit] = {
                    "surrounding_qubits": surrounding_qubits,
                    "remove": [],
                }
                # Bottom row
                if y == 0:
                    if x%2 == 0:
                        if surrounding_qubits["left"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B2")
                        if surrounding_qubits["right"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B1")
                        if surrounding_qubits["top"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B0")
                    else:
                        if surrounding_qubits["left"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B0")
                        if surrounding_qubits["right"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B3")
                        if surrounding_qubits["top"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B1")
                # Top row
                elif y == (N_y - 1):
                    if x%2 == 0:
                        if surrounding_qubits["left"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B2")
                        if surrounding_qubits["right"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B1")
                        if surrounding_qubits["bottom"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B3")
                    else:
                        if surrounding_qubits["left"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B0")
                        if surrounding_qubits["right"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B3")
                        if surrounding_qubits["bottom"] == -1:
                            pins_to_remove[current_qubit]["remove"].append("B2")
                # Middle row
                else:
                    if x%2 == 0:
                        if (y-1)%2 == 0:
                            if surrounding_qubits["left"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B0")
                            if surrounding_qubits["right"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B3")
                            if surrounding_qubits["bottom"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B2")
                            if surrounding_qubits["top"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B1")
                        else:
                            if surrounding_qubits["left"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B2")
                            if surrounding_qubits["right"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B1")
                            if surrounding_qubits["bottom"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B3")
                            if surrounding_qubits["top"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B0")                        
                    else:
                        if (y-1)%2 == 0:
                            if surrounding_qubits["left"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B2")
                            if surrounding_qubits["right"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B1")
                            if surrounding_qubits["bottom"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B3")
                            if surrounding_qubits["top"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B0")
                        else:
                            if surrounding_qubits["left"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B0")
                            if surrounding_qubits["right"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B3")
                            if surrounding_qubits["bottom"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B2")
                            if surrounding_qubits["top"] == -1:
                                pins_to_remove[current_qubit]["remove"].append("B1")                        

        return pins_to_remove

    def _get_qubit(self, qubit_grid: np.array, row: int, col: int, default_value: int = -1) -> int:
        if row < 0 or row >= qubit_grid.shape[0] or col < 0 or col >= qubit_grid.shape[1]:
            value = default_value
        else:
            value = qubit_grid[row, col]
        return value
                