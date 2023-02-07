from mqhad.architecture_generator.layout import Layout


class TestLayout:
    def test_get_layout(self):
        layout = Layout()
        ordered_degree = [(4, 5), (0, 3), (1, 2), (2, 1), (3, 1)]
        adjacency_matrix = [
            [0, 1, 0, 0, 2],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [2, 1, 1, 1, 0],
        ]
        dimX = 3
        dimY = 3
        qubit_grid = [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]]
        assert (dimX, dimY, qubit_grid) == layout.get_layout(
            ordered_degree, adjacency_matrix
        )
