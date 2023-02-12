from collections import OrderedDict
from ..qubit_connector_base import QubitConnectorBase
from qiskit_metal import Dict
from qiskit_metal.designs import DesignPlanar
from qiskit_metal.qlibrary.tlines.meandered import RouteMeander
from qiskit_metal.analyses.em.cpw_calculations import guided_wavelength
import numpy as np


class RouteMeanderConnector(QubitConnectorBase):
    def __init__(
        self,
        design: DesignPlanar = None,
        qubit_grid: np.ndarray = np.array([]),
        qubit_frequencies: np.ndarray = np.array([]),
    ):
        self._design = design
        self.qubit_frequencies = qubit_frequencies
        self._qubit_grid = qubit_grid

    def generate_qubit_connection(self) -> list[tuple[list[str, str], RouteMeander]]:
        N_x = len(self._qubit_grid[0])
        N_y = len(self._qubit_grid)
        resonators = []

        for x in range(N_x):
            for y in range(N_y):
                # "upward" connection, avoids drawing connectors for 'top' row. Changes connector length by +/-50um to avoid frequency collisions
                current_qubit = self._qubit_grid[y][x]

                # No qubit in grid
                if current_qubit == -1:
                    continue

                current_qubit_frequency = self.qubit_frequencies[current_qubit]

                # Estimate for resonator length. Simulation needs to be done for more accurate length
                resonator_length = self._find_resonator_length(
                    frequency=current_qubit_frequency, line_width=10, line_gap=6, N=2
                )

                if y < (N_y - 1):
                    top_qubit = self._qubit_grid[y + 1][x]

                    if top_qubit != -1:
                        (
                            vertical_start_pin_ref,
                            vertical_end_pin_ref,
                            meander_asymmetry,
                        ) = self._get_upward_connection_configuration(x, y)

                        connectorAD = RouteMeander(
                            self._design,
                            f"CU_{current_qubit}_{top_qubit}",
                            options=dict(
                                total_length=resonator_length,  # str(7)+'mm',
                                fillet="99um",
                                lead=dict(
                                    start_straight="0.5mm", end_straight="0.25mm"
                                ),
                                meander=dict(asymmetry=meander_asymmetry),
                                pin_inputs=dict(
                                    start_pin=dict(
                                        component=f"Q_{current_qubit}",
                                        pin=vertical_start_pin_ref,
                                    ),
                                    end_pin=dict(
                                        component=f"Q_{top_qubit}",
                                        pin=vertical_end_pin_ref,
                                    ),
                                ),
                            ),
                        )

                        resonators.append(
                            ([f"Q_{current_qubit}", f"Q_{top_qubit}"], connectorAD)
                        )

                # "sideways" connection, avoids drawing for far right col. Changes connector length by +/- 25um
                # to avoid frequency collisions
                if x < (N_x - 1):
                    right_qubit = self._qubit_grid[y][x + 1]

                    if right_qubit != -1:
                        (
                            horizontal_start_pin_ref,
                            horizontal_end_pin_ref,
                            jogs_start,
                        ) = self._get_sideway_connection_configuration(x, y)

                        connectorBC = RouteMeander(
                            self._design,
                            f"CS_{current_qubit}_{right_qubit}",
                            options=dict(
                                total_length=resonator_length,  # str(6)+'mm',
                                fillet="99um",
                                lead=Dict(
                                    start_jogged_extension=jogs_start,
                                    start_straight="0.3mm",
                                    end_straight="0.4mm",
                                ),  #'0.25mm'),
                                meander=Dict(asymmetry="-200um"),
                                pin_inputs=Dict(
                                    start_pin=Dict(
                                        component=f"Q_{current_qubit}",
                                        pin=horizontal_start_pin_ref,
                                    ),
                                    end_pin=Dict(
                                        component=f"Q_{right_qubit}",
                                        pin=horizontal_end_pin_ref,
                                    ),
                                ),
                            ),
                        )
                        resonators.append(
                            ([f"Q_{current_qubit}", f"Q_{right_qubit}"], connectorBC)
                        )

        return resonators

    def _get_upward_connection_configuration(self, x, y):
        if x % 2 == 0:
            if y % 2 == 0:
                vertical_start_pin_ref = "B0"
                vertical_end_pin_ref = "B2"
                meander_asymmetry = "700um"
            else:
                vertical_start_pin_ref = "B1"
                vertical_end_pin_ref = "B3"
                meander_asymmetry = "-700um"
        else:
            if y % 2 == 0:
                vertical_start_pin_ref = "B1"
                vertical_end_pin_ref = "B3"
                meander_asymmetry = "-700um"
            else:
                vertical_start_pin_ref = "B0"
                vertical_end_pin_ref = "B2"
                meander_asymmetry = "700um"
        return vertical_start_pin_ref, vertical_end_pin_ref, meander_asymmetry

    def _get_sideway_connection_configuration(self, x, y):
        if y % 2 == 0:
            # even lines, [0,2,...]
            if x % 2 == 0:
                # up side-ways
                horizontal_start_pin_ref = "B1"
                horizontal_end_pin_ref = "B0"
                jogs_start = OrderedDict()
                jogs_start[0] = ["R", "150um"]

            else:
                # botton side-ways
                horizontal_start_pin_ref = "B3"
                horizontal_end_pin_ref = "B2"
                jogs_start = OrderedDict()
                # jogs_start[0] = ["L", '200um']
        else:
            # odd lines, [1,3,...]
            if x % 2 == 0:
                # bottom side-ways
                horizontal_start_pin_ref = "B3"
                horizontal_end_pin_ref = "B2"
                jogs_start = OrderedDict()
                # jogs_start[0] = ["L", '200um']
            else:
                # up side-ways
                horizontal_start_pin_ref = "B1"
                horizontal_end_pin_ref = "B0"
                jogs_start = OrderedDict()
                jogs_start[0] = ["R", "150um"]
        return horizontal_start_pin_ref, horizontal_end_pin_ref, jogs_start

    def _find_resonator_length(self, frequency, line_width, line_gap, N):
        # frequency in GHz
        # line_width/line_gap in um
        # N -> 2 for lambda/2, 4 for lambda/4
        # substrate dimensions and properties already set

        [lambdaG, etfSqrt, q] = guided_wavelength(
            frequency * 10**9,
            line_width * 10**-6,
            line_gap * 10**-6,
            750 * 10**-6,
            200 * 10**-9,
            11.9,
        )
        return str(lambdaG / N * 10**3) + "mm"
