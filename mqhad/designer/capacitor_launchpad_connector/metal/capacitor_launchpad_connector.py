from ..capacitor_launchpad_connector_base import CapacitorLaunchpadConnectorBase
from qiskit_metal import Dict
from qiskit_metal.designs import DesignPlanar
from qiskit_metal.qlibrary.tlines.pathfinder import RoutePathfinder
import numpy as np


class CapacitorLaunchpadConnector(CapacitorLaunchpadConnectorBase):
    def __init__(self, design: DesignPlanar = None, qubit_grid: np.ndarray = np.array([])):
        self._design = design
        self._qubit_grid = qubit_grid

    def generate_capacitor_launchpad_connection(
        self,
    ) -> list[tuple[list[str, str], RoutePathfinder]]:
        N_x = len(self._qubit_grid[0])
        N_y = len(self._qubit_grid)
        tl_readouts = []
        # Loop to generate and draw the launchpads
        for x in range(N_x):
            for y in range(N_y):
                current_qubit = self._qubit_grid[y][x]

                # Skip readout if no qubit at position
                if current_qubit == -1:
                    continue

                # Bottom row
                if y == 0:
                    start_pin_ = "south_end"
                # Top row
                elif y == (N_y - 1):
                    start_pin_ = "north_end"
                # Middle row
                else:
                    start_pin_ = "south_end"
                end_pin_ = "tie"

                tl_readout = RoutePathfinder(
                    self._design,
                    f"TL_Readout_{current_qubit}",
                    options=dict(
                        hfss_wire_bonds=True,
                        pin_inputs=Dict(
                            start_pin=Dict(
                                component=f"Cap_Readout_{current_qubit}", pin=start_pin_
                            ),
                            end_pin=Dict(
                                component=f"Launch_Readout_{current_qubit}",
                                pin=end_pin_,
                            ),
                        ),
                    ),
                )

                tl_readouts.append(
                    [
                        (
                            f"Cap_Readout_{current_qubit}",
                            f"Launch_Readout_{current_qubit}",
                        ),
                        tl_readout,
                    ]
                )

        return tl_readouts
