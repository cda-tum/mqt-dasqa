import sys
from unittest.mock import MagicMock
from mqhad.designer.design import Design
import numpy as np


class TestDesign:
    def test_design(self):
        design = Design()
        design._design_metal = MagicMock()
        design.design()
        design._design_metal.assert_called_once()

    # Test for no exception
    def test_design_metal(self, monkeypatch):
        # In this example, we define a exit_noop() function
        # that simply does nothing, and then use the monkeypatch.setattr()
        # method to replace the sys.exit() function with exit_noop() during the test.
        # This way, if the program calls sys.exit(), it will be replaced with the
        # no-op function and the test will continue to run instead of exiting.
        def exit_noop(status):
            pass

        # replace sys.exit with exit_noop
        monkeypatch.setattr(sys, "exit", exit_noop)

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
        design = Design(
            design_backend="metal",
            qubit_grid=qubit_grid,
            qubit_frequencies=qubit_frequencies,
        )
        design._design_metal()
