import numpy as np
from .bus_base import BusBase


class Bus(BusBase):
    def __init__(
        self,
        dimX: int = 0,
        dimY: int = 0,
        qubit_grid: np.ndarray = np.array([]),
        adjacency_matrix: np.ndarray = np.array([]),
        num_4Q_bus: int = 10,
    ):
        self.dimX = dimX
        self.dimY = dimY
        self.qubit_grid = qubit_grid
        self.adjacency_matrix = adjacency_matrix
        self.num_4Q_bus = num_4Q_bus

    def bus_select(self) -> tuple[np.ndarray, np.ndarray]:
        bus_locations_4Q = []

        bus_grid = np.zeros((self.dimX - 1, self.dimY - 1), dtype=int)
        # Sum of weights across diagonals of qubits
        # For the example in Figure 7 (c), the cross-coupling weight of the green square is the
        # coupling strength of q0,q3 plus that of q1,q2.
        bus_weights = self._calculate_cross_coupling_weights(
            self.dimX, self.dimY, self.qubit_grid, self.adjacency_matrix
        )

        while self.num_4Q_bus > 0:
            # However, the cross-coupling weight is not accurate enough
            # to evaluate the benefit of 4-qubit for a square because the prohibited condition is not yet considered.
            filtered_weights = self._calculate_filtered_weights(
                self.dimX, self.dimY, bus_weights
            )

            # After applying the filter, we will select one square with the highest filtered weight.
            select_X = -1
            select_Y = -1
            select_weight = -100000000
            for x in range(self.dimX - 1):
                for y in range(self.dimY - 1):
                    if bus_weights[x][y] > 0:
                        if filtered_weights[x][y] > select_weight:
                            select_X = x
                            select_Y = y
                            select_weight = filtered_weights[x][y]

            # Break if no suitable position anymore for 4-qubit buses.
            # The algorithm will iterate again to select the next square until
            # there are not more squares available or we have already applied enough number of 4-qubit buses.
            if select_X == -1:
                break

            bus_locations_4Q.append([select_X + 1, select_Y + 1])
            bus_grid[select_X][select_Y] = 1

            # We also change their weights to zero because they should not affect the 4-qubit selection among the remaining squares.
            bus_weights[select_X][select_Y] = 0
            if select_X != 0:
                bus_weights[select_X - 1][select_Y] = 0
            if select_X != (self.dimX - 2):
                bus_weights[select_X + 1][select_Y] = 0
            if select_Y != 0:
                bus_weights[select_X][select_Y - 1] = 0
            if select_Y != (self.dimY - 2):
                bus_weights[select_X][select_Y + 1] = 0

            self.num_4Q_bus -= 1
        bus_locations_4Q = np.array(bus_locations_4Q)
        return bus_grid, bus_locations_4Q

    def _calculate_filtered_weights(
        self, dimX: int, dimY: int, bus_weights: np.ndarray
    ) -> np.ndarray:
        """Calculate filtered weight.

        Args:
            dimX (int): dimension X
            dimY (int): dimension Y
            bus_weights (np.ndarray): bus weights

        Returns:
            np.ndarray: filtered weights
        """
        filtered_weights = np.zeros((dimX - 1, dimY - 1), dtype=int)
        for x in range(dimX - 1):
            for y in range(dimY - 1):
                weight = bus_weights[x][y]
                if x != 0:
                    weight -= bus_weights[x - 1][y]
                if y != 0:
                    weight -= bus_weights[x][y - 1]
                if y != (self.dimY - 2):
                    weight -= bus_weights[x][y + 1]
                if x != (self.dimX - 2):
                    weight -= bus_weights[x + 1][y]
                filtered_weights[x][y] = weight
        return filtered_weights

    def _calculate_cross_coupling_weights(
        self, dimX: int, dimY: int, qubit_grid: np.ndarray, adjacency_matrix: np.ndarray
    ) -> np.ndarray:
        """Calculate cross coupling weight.

        Args:
            dimX (int): dimension X
            dimY (int): dimension Y
            qubit_grid (np.ndarray): qubit grid
            adjacency_matrix (np.ndarray): adjacency matrix

        Returns:
            np.ndarray: bus weights
        """
        bus_weights = np.zeros((dimX - 1, dimY - 1), dtype=int)
        for x in range(dimX - 1):
            for y in range(dimY - 1):
                weight = 0
                if (qubit_grid[x][y] != -1) and (qubit_grid[x + 1][y + 1] != -1):
                    weight += adjacency_matrix[qubit_grid[x][y]][
                        qubit_grid[x + 1][y + 1]
                    ]
                if (qubit_grid[x][y + 1] != -1) and (qubit_grid[x + 1][y] != -1):
                    weight += adjacency_matrix[qubit_grid[x][y + 1]][
                        qubit_grid[x + 1][y]
                    ]
                bus_weights[x][y] = weight
        return bus_weights
