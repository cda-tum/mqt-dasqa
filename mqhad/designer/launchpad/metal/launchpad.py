from ..launchpad_base import LaunchpadBase
from qiskit_metal.designs import DesignPlanar
from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond
import numpy as np


class Launchpad(LaunchpadBase):
    def __init__(
        self, design: DesignPlanar = None, qubit_grid: np.ndarray = np.array([])
    ):
        self._design = design
        self._qubit_grid = qubit_grid

    def generate_launchpad(self) -> list[list[LaunchpadWirebond]]:
        N_x = len(self._qubit_grid[0])
        N_y = len(self._qubit_grid)
        launchpads = {}
        # Loop to generate and draw the launchpads
        for x in range(N_x):
            for y in range(N_y):
                current_qubit = self._qubit_grid[y][x]

                # Skip readout if no qubit at position
                if current_qubit == -1:
                    continue

                pos_x, pos_y, orientation = self._get_configuration(N_y, x, y)

                launchpad_name = f"Launch_Readout_{current_qubit}"

                launchpad = LaunchpadWirebond(
                    self._design,
                    launchpad_name,
                    options=dict(pos_x=pos_x, pos_y=pos_y, orientation=orientation),
                )
                launchpads[launchpad_name] = launchpad

        return launchpads

    def _get_configuration(self, N_y, x, y):
        x_loc = 3500
        y_loc = 3000
        # Bottom row
        if y == 0:
            offset_x = 150
            offset_y = 500
            if x % 2 == 0:
                pos_x = str(x * x_loc + offset_x) + "um"
            else:
                pos_x = str(x * x_loc - offset_x) + "um"
            pos_y = str(-y_loc / 2 - offset_y) + "um"
            orientation = "90"
            # Top row
        elif y == (N_y - 1):
            offset_x = 150
            offset_y = 500
            if x % 2 == 0:
                pos_x = str(x * x_loc - offset_x) + "um"
            else:
                pos_x = str(x * x_loc + offset_x) + "um"
            pos_y = str(y * y_loc + y_loc / 2 + offset_y) + "um"
            orientation = "-90"
        else:
            pos_x = str(x * x_loc - x_loc / 2) + "um"
            pos_y = str(y * y_loc) + "um"
            orientation = "0"
        return pos_x, pos_y, orientation
