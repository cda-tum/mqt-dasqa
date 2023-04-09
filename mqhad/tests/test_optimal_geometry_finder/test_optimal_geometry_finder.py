from unittest.mock import patch, MagicMock
from sklearn.pipeline import Pipeline
import os


class TestOptimalGeometryFinder:
    @patch("builtins.open")
    @patch("pickle.load")
    def test_unpack_model(self, mock_load, mock_open):
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

        from mqhad.optimal_geometry_finder.optimal_geometry_finder import (
            OptimalGeometryFinder,
        )

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

    def test_unpack_models2(self):
        # Real model file is used
        from mqhad.optimizer.metal import Optimizer

        models = {
            "qubit": {
                "fQ": {
                    "pad_gap": os.getcwd()
                    + "/mqhad/tests/test_model/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                }
            },
            "resonator": None,
        }

        from mqhad.optimal_geometry_finder.optimal_geometry_finder import (
            OptimalGeometryFinder,
        )

        class OptimalGeometryFinderMock(OptimalGeometryFinder):
            def __init__(self):
                pass

        optimal_geometry_finder = OptimalGeometryFinderMock()
        optimal_geometry_finder._models = models
        unpacked_models = optimal_geometry_finder._unpack_models()
        assert type(unpacked_models["qubit"]["fQ"]["pad_gap"]) == Pipeline

    def test_find_optimal_geometry(self):
        from mqhad.optimal_geometry_finder.optimal_geometry_finder import (
            OptimalGeometryFinder,
        )

        class OptimalGeometryFinderMock(OptimalGeometryFinder):
            def __init__(self):
                pass

        optimal_geometry_finder = OptimalGeometryFinderMock()
        mock_concrete_optimal_geometry_finder = MagicMock()
        return_value = {
            "pad_gap": "10.0um",
            "pad_height": "10.0um",
        }
        mock_concrete_optimal_geometry_finder.find_optimal_geometry.return_value = return_value
        optimal_geometry_finder._optimal_geometry_finder = mock_concrete_optimal_geometry_finder
        optimal_geometry = optimal_geometry_finder.find_optimal_geometry(
            "qubit", "fQ", 0.1
        )
        assert optimal_geometry == return_value
