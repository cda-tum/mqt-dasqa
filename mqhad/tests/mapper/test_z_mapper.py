from unittest.mock import MagicMock
import numpy as np


# Need to be last tests executed for desinger module
# because it import Design without patching
class TestZMapper:
    def test_design(self):
        from mqhad.mapper.mapper import Mapper

        design = Mapper()
        design._map_metal = MagicMock()
        design.map()
        design._map_metal.assert_called_once()

    # Test for no exception
    def test_design_metal(self):
        from mqhad.mapper.mapper import Mapper

        qubit_grid = np.array(
            [
                [-1, -1, -1, 0, -1, -1, -1, 1, -1, -1, -1],
                [-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                [-1, 12, -1, -1, -1, 13, -1, -1, -1, 14, -1],
                [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, -1],
                [-1, -1, -1, 25, -1, -1, -1, 26, -1, -1, -1],
            ]
        )
        qubit_frequencies = np.linspace(5.0, 5.1, 27)
        design = Mapper(
            design_backend="metal",
            qubit_grid=qubit_grid,
            qubit_frequencies=qubit_frequencies,
        )
        design._map_metal()
