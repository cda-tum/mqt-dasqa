from unittest import mock
from sklearn.pipeline import Pipeline
import os


class TestOptimalGeometryFinder:
    @mock.patch("builtins.open")
    @mock.patch("pickle.load")
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

        from mqhad.optimal_geometry_finder.optimal_geometry_finder import OptimalGeometryFinder
        
        class OptimalGeometryFinderMock(OptimalGeometryFinder):
            def __init__(self):
                pass

        optimal_geometry_finder = OptimalGeometryFinderMock()
        optimal_geometry_finder._models = models
        unpacked_models = optimal_geometry_finder._unpack_models()
        assert type(unpacked_models["qubit"]["fQ"]["pad_gap"]) == Pipeline
    
    def test_find_optimal_geometry(self):
        from mqhad.optimal_geometry_finder.optimal_geometry_finder import OptimalGeometryFinder
        
        class OptimalGeometryFinderMock(OptimalGeometryFinder):
            def __init__(self):
                pass

        optimal_geometry_finder = OptimalGeometryFinderMock()
        optimal_geometry_finder._models = {
            "qubit": {
                "fQ": {
                    "pad_gap": "model_unpacked",
                    "pad_height": "model_unpacked",
                }
            },
            "resonator": None,
        }
        optimal_geometry = optimal_geometry_finder.find_optimal_geometry("qubit", "fQ", "pad_gap", 0.1)
        assert optimal_geometry == 0.1