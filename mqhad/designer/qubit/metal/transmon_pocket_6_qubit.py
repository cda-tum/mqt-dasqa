from collections import OrderedDict
from ..qubit_base import QubitBase
from qiskit_metal.designs import DesignPlanar
from qiskit_metal.qlibrary.qubits.transmon_pocket_6 import TransmonPocket6
import numpy as np


class TransmonPocket6Qubit(QubitBase):
    def __init__(
        self, design: DesignPlanar = None, qubit_grid: np.ndarray = np.array([])
    ):
        self._design = design
        self._qubit_grid = qubit_grid

    def generate_qubit_layout(self):
        self._pins_to_remove = self._get_open_qubit_pins(self._qubit_grid)
        self.qubits = self._generate_qubits(self._design, self._qubit_grid, self._pins_to_remove)
        return self.qubits

    def _generate_qubits(self, design: DesignPlanar, qubit_grid: np.ndarray, pins_to_remove: dict[int,dict[str,list[str]]]):
        """Generate layout of qubits in the chip

        Returns:
            dict[str, TransmonPocket]: dict of qubit objects
        """
        N_x = len(qubit_grid[0])
        N_y = len(qubit_grid)
        qubits = {}
        #Loop to generate and draw the qubits
        for x in range(N_x):
            for y in range(N_y):
                current_qubit = qubit_grid[y][x]

                # No qubit in grid
                if current_qubit == -1:
                    continue
                
                qubit_name = f'Q_{current_qubit}'

                connection_pads = dict(
                    B0 = dict(loc_W=-1, loc_H=-1, pad_width='75um'),
                    B1  = dict(loc_W=-1, loc_H=+1, pad_width='120um'),
                    B2  = dict(loc_W=+1, loc_H=-1, pad_width='120um'),
                    B3 = dict(loc_W = +1, loc_H = +1, pad_width='90um'),
                )

                if pins_to_remove is not None:
                    # TODO: Creating a dictionary seems unnecessary
                    exclude_pin_dict = {pin: dict() for pin in pins_to_remove[current_qubit]["remove"]}
                    connection_pins = set(connection_pads) - set(exclude_pin_dict.keys())
                    connection_pads_intersected = {key: connection_pads[key] for key in connection_pins}
                else:
                    connection_pads_intersected = connection_pads

                #TODO: What should be the correct spacing between qubits
                options = dict(pos_x= str(x*3500)+'um', pos_y = str(y*3000)+'um', orientation = "-90",
                connection_pads=connection_pads_intersected)
                
                if y != 0 and y != (N_y-1):
                    options["connection_pads"]["B4"] = dict(loc_W=0, loc_H=-1, pad_width='90um')
                
                obj=TransmonPocket6(design,qubit_name,options)
                qubits[qubit_name] = obj
        return qubits

    def _get_open_qubit_pins(self, qubit_grid: np.ndarray[int]) -> dict[int,list[str]]:

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
                