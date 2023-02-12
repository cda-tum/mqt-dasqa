from unittest.mock import patch
import numpy as np


class TestMetalLaunchpad:
    def test_generate_launchpad(self):
        with patch(
            "qiskit_metal.qlibrary.terminations.launchpad_wb.LaunchpadWirebond"
        ) as mock_class:
            from mqhad.designer.launchpad.metal import Launchpad

            mock_class.return_value = object
            qubit_grid = np.array(
                [
                    [-1, -1, -1, 0, -1, -1, -1, 1, -1, -1, -1],
                    [-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                    [-1, 12, -1, -1, -1, 13, -1, -1, -1, 14, -1],
                    [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, -1],
                    [-1, -1, -1, 25, -1, -1, -1, 26, -1, -1, -1],
                ]
            )
            launchpad = Launchpad(qubit_grid=qubit_grid)
            launchpads = launchpad.generate_launchpad()
            assert len(launchpads) == 27

    def test_get_configuration(self):
        pass
