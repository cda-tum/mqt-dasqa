from unittest.mock import patch, MagicMock
import os


class TestOptimalGeometryFinder:
    def test_unpack_model(self):
        with patch("builtins.open"), patch("pickle.load") as mock_load:
            mock_load.return_value = "model_unpacked"

            models = {
                "qubit": {
                    "fQ": {
                        "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                        "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                    }
                },
                "resonator": None,
            }


            from mqhad.optimal_geometry_finder.optimal_geometry_finder import OptimalGeometryFinder
            
            class OptimalGeometryFinderMock(OptimalGeometryFinder):
                def __init__(self):
                    pass

            optimal_geometry_finder = OptimalGeometryFinderMock()
            optimal_geometry_finder._models = models
            unpacked_models = optimal_geometry_finder._unpack_models()
            assert unpacked_models == {
                "qubit": {
                    "fQ": {
                        "pad_gap": "model_unpacked",
                        "pad_height": "model_unpacked",
                    }
                },
                "resonator": None,
            }
