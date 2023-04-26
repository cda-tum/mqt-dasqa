import numpy as np
from src.architecture_generator1.bus import Bus


class TestBus:
    def test_bus(self):
        dimX = 3
        dimY = 3
        qubit_grid = np.array([[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])
        adjacency_matrix = np.array(
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ]
        )
        bus = Bus(
            dimX=dimX,
            dimY=dimY,
            qubit_grid=qubit_grid,
            adjacency_matrix=adjacency_matrix,
            num_4Q_bus=10,
        )
        bus_grid = [[0, 0], [0, 1]]
        bus_location = [[2, 2]]
        bus_grid, bus_location = bus.bus_select()
        np.testing.assert_array_equal(bus_grid, [[0, 0], [0, 1]])
        np.testing.assert_array_equal(bus_location, [(2, 2)])

    def test_calculate_cross_coupling_weight(self):
        dimX = 3
        dimY = 3
        qubit_grid = np.array([[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])
        adjacency_matrix = np.array(
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ]
        )
        bus = Bus(
            dimX=dimX,
            dimY=dimY,
            qubit_grid=qubit_grid,
            adjacency_matrix=adjacency_matrix,
            num_4Q_bus=10,
        )
        bus_weights = bus._calculate_cross_coupling_weights(
            dimX, dimY, qubit_grid, adjacency_matrix
        )
        np.testing.assert_array_equal(bus_weights, [[0, 0], [0, 1]])

    def test_calculate_filtered_weights(self):
        dimX = 3
        dimY = 3
        qubit_grid = np.array([[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])
        adjacency_matrix = np.array(
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ]
        )
        bus = Bus(
            dimX=dimX,
            dimY=dimY,
            qubit_grid=qubit_grid,
            adjacency_matrix=adjacency_matrix,
            num_4Q_bus=10,
        )

        bus_weights = np.array([[0, 0], [0, 1]])
        filtered_weights = bus._calculate_filtered_weights(dimX, dimY, bus_weights)
        np.testing.assert_array_equal(filtered_weights, [[0, -1], [-1, 1]])
