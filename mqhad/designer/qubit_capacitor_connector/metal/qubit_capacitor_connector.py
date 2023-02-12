from collections import OrderedDict
from ..qubit_capacitor_connector_base import QubitCapacitorConnectorBase
from qiskit_metal import Dict
from qiskit_metal.designs import DesignPlanar
from qiskit_metal.qlibrary.tlines.pathfinder import RoutePathfinder

import numpy as np


class QubitCapacitorConnector(QubitCapacitorConnectorBase):
    def __init__(self, design: DesignPlanar = None, qubit_grid: np.ndarray = np.array([])):
        self._design = design
        self._qubit_grid = qubit_grid

    def generate_qubit_capacitor_connection(self):
        N_x = len(self._qubit_grid[0])
        N_y = len(self._qubit_grid)
        meanders = []
        # Loop to generate and draw the launchpads
        for x in range(N_x):
            for y in range(N_y):
                current_qubit = self._qubit_grid[y][x]

                # Skip readout if no qubit at position
                if current_qubit == -1:
                    continue

                x_loc = 3500
                y_loc = 3000
                # Bottom row
                if y == 0:
                    offset_readout_capacitor = 100
                    offset_anchor = 100
                    if x % 2 == 0:
                        start_pin_ = "B3"
                        pos_x = (x * x_loc + x_loc / 2 - offset_anchor) / 1000
                    else:
                        start_pin_ = "B2"
                        pos_x = (x * x_loc - x_loc / 2 + offset_anchor) / 1000
                    pos_y = ((-y_loc / 2 - offset_readout_capacitor) / 2) / 1000
                    pin_loc = "north_end"
                # Top row
                elif y == (N_y - 1):
                    offset_readout_capacitor = 100
                    offset_anchor = 100
                    if x % 2 == 0:
                        start_pin_ = "B0"
                        pos_x = (x * x_loc - x_loc / 2 + offset_anchor) / 1000
                    else:
                        start_pin_ = "B1"
                        pos_x = (x * x_loc + x_loc / 2 - offset_anchor) / 1000
                    pos_y = (
                        y * y_loc + (y_loc / 2 + offset_readout_capacitor) / 2
                    ) / 1000
                    pin_loc = "south_end"
                # Middle row
                else:
                    start_pin_ = "B4"
                    pin_loc = "north_end"
                    offset_readout_capacitor = 300
                    pos_x = (
                        x * x_loc - ((x_loc / 2 - offset_readout_capacitor) / 2)
                    ) / 1000
                    if x % 2 == 0:
                        pos_y = (y * y_loc - y_loc / 2 + y_loc / 4) / 1000
                    else:
                        pos_y = (y * y_loc + y_loc / 2 - y_loc / 4) / 1000

                anchors = OrderedDict()
                anchors[0] = np.array([pos_x, pos_y])

                meander = RoutePathfinder(
                    self._design,
                    f"Readout_{current_qubit}",
                    options=dict(
                        hfss_wire_bonds=True,
                        pin_inputs=Dict(
                            start_pin=Dict(
                                component=f"Q_{current_qubit}", pin=start_pin_
                            ),
                            end_pin=Dict(
                                component=f"Cap_Readout_{current_qubit}", pin=pin_loc
                            ),
                        ),
                        lead=Dict(
                            start_straight="200um",
                            end_straight="200um",
                        ),
                        fillet="90um",
                        step_size="0.25mm",
                        anchors=anchors,
                        # meander=Dict(
                        #     asymmetry = '-200um',
                        #     lead_direction_inverted='true'),
                        # avoid_collision=False,
                        # total_length = '3mm', #'8.3mm'))
                    ),
                )

                meanders.append(
                    ([f"Q_{current_qubit}", f"Cap_Readout_{current_qubit}"], meander)
                )
        return meanders
