import numpy as np
from mqhad.designer.qubit import QubitMetal


class TestQubitMetal:
    def test_generate_qubit_layout(self):
        pass

    # Write test case for _get_qubit
    def test_get_qubit(self):
        qubit_grid = np.array(
            [
                [-1, -1, -1, 0, -1, -1, -1, 1, -1, -1, -1],
                [-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                [-1, 12, -1, -1, -1, 13, -1, -1, -1, 14, -1],
                [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, -1],
                [-1, -1, -1, 25, -1, -1, -1, 26, -1, -1, -1],
            ]
        )
        qubit = QubitMetal()
        assert 0 == qubit._get_qubit(qubit_grid, 0, 3)
        assert -1 == qubit._get_qubit(qubit_grid, 0, 0)
        assert -1 == qubit._get_qubit(qubit_grid, -1, 1)
        assert -1 == qubit._get_qubit(qubit_grid, 1, -1)
        assert -1 == qubit._get_qubit(qubit_grid, qubit_grid.shape[0] + 1, 5)
        assert -1 == qubit._get_qubit(qubit_grid, 5, qubit_grid.shape[1] + 1)
