import os
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
    def test_design_metal(self):
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
        config = {
            "model": {
                "qubit": {
                    "fQ": {
                        "pad_gap": os.getcwd()
                        + "/mqhad/tests/test_model/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                    }
                },
                "resonator": None,
            },
            "target": {
                "qubit": {"specific": {"Q_0": {"fQ": 5.3}}, "general": None},
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        design = Design(
            design_backend="metal",
            qubit_grid=qubit_grid,
            qubit_frequencies=qubit_frequencies,
            display_gui=True,
            config=config,
        )
        design._design_metal(display_gui=True)
