import numpy as np
from mqhad.architecture_generator.layout import Layout


class TestLayout:
    def test_get_layout(self):
        ordered_degree = np.array([[4, 5], [0, 3], [1, 2], [2, 1], [3, 1]])
        adjacency_matrix = np.array(
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ]
        )
        layout = Layout(
            ordered_degree=ordered_degree, adjacency_matrix=adjacency_matrix
        )
        dimX, dimY, qubit_grid = layout.get_layout()
        assert dimX == 3
        assert dimY == 3
        np.testing.assert_array_equal(qubit_grid, [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])

    def test_get_layout_with_1_qubit(self):
        ordered_degree = np.array([(0, 1)])
        adjacency_matrix = np.array([[0]])
        layout = Layout(
            ordered_degree=ordered_degree, adjacency_matrix=adjacency_matrix
        )
        dimX, dimY, qubit_grid = layout.get_layout()
        assert dimX == 1
        assert dimY == 1
        np.testing.assert_array_equal(qubit_grid, [[0]])

    def test_extract_min_max_XY(self):
        layout = Layout()
        assigned_qubit_list = [[4, 0, 0], [0, 0, 1], [1, 1, 0], [2, -1, 0], [3, 0, -1]]
        minX = -1
        minY = -1
        maxX = 1
        maxY = 1
        assert (minX, minY, maxX, maxY) == layout._extract_min_max_XY(
            assigned_qubit_list
        )

    def test_center_layout(self):
        layout = Layout()
        assigned_qubit_list = np.array(
            [[4, 0, 0], [0, 0, 1], [1, 1, 0], [2, -1, 0], [3, 0, -1]]
        )
        dimX, dimY, qubit_grid = layout._center_layout(
            assigned_qubit_list,
            -1,
            -1,
            1,
            1,
        )
        assert dimX == 3
        assert dimY == 3
        np.testing.assert_array_equal(qubit_grid, [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])

    def test_calculate_distance_to_assigned_qubit(self):
        adjacency_matrix = np.array(
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ]
        )
        layout = Layout(ordered_degree=None, adjacency_matrix=adjacency_matrix)
        candidate_qubit = np.array([4, 5])
        assigned_qubit = np.array([0, 0, 1])
        location = np.array([0, 0])
        assert 2.01 == layout._calculate_distance_to_assigned_qubits(
            candidate_qubit, assigned_qubit, location
        )
        location = np.array([0, 1])
        assert 0.0 == layout._calculate_distance_to_assigned_qubits(
            candidate_qubit, assigned_qubit, location
        )
        location = np.array([1, 1])
        assert 2.01 == layout._calculate_distance_to_assigned_qubits(
            candidate_qubit, assigned_qubit, location
        )
        location = np.array([1, 0])
        assert 4.02 == layout._calculate_distance_to_assigned_qubits(
            candidate_qubit, assigned_qubit, location
        )
