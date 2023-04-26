from unittest.mock import patch, MagicMock
import os
from sklearn.pipeline import Pipeline


class TestOptimalStatisticalGeometryFinder:
    @patch("builtins.open")
    @patch("pickle.load")
    def test_unpack_model(self, mock_load, mock_open):
        from src.optimal_geometry_finder.statistical_model.optimal_geometry_finder import (
            OptimalGeometryFinder as OptimalStatisticalGeometryFinder,
        )

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

        class OptimalStatisticalGeometryFinderMock(OptimalStatisticalGeometryFinder):
            def __init__(self):
                pass

        optimal_geometry_finder = OptimalStatisticalGeometryFinderMock()
        optimal_geometry_finder._models_config = models
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
        from src.optimal_geometry_finder.statistical_model.optimal_geometry_finder import (
            OptimalGeometryFinder as OptimalStatisticalGeometryFinder,
        )

        models = {
            "qubit": {
                "fQ": {
                    "pad_gap": os.getcwd()
                    + "/src/tests/test_model/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                }
            },
            "resonator": None,
        }

        class OptimalStatisticalGeometryFinderMock(OptimalStatisticalGeometryFinder):
            def __init__(self):
                pass

        optimal_geometry_finder = OptimalStatisticalGeometryFinderMock()
        optimal_geometry_finder._models_config = models
        unpacked_models = optimal_geometry_finder._unpack_models()
        assert type(unpacked_models["qubit"]["fQ"]["pad_gap"]) == Pipeline

    def test_find_optimal_geometry(self):
        from src.optimal_geometry_finder.statistical_model.optimal_geometry_finder import (
            OptimalGeometryFinder as OptimalStatisticalGeometryFinder,
        )

        class OptimalStatisticalGeometryFinderMock(OptimalStatisticalGeometryFinder):
            def __init__(self):
                pass

        optimal_statistical_geometry_finder = OptimalStatisticalGeometryFinderMock()
        mock_model = MagicMock()
        return_value = [10.0]
        mock_model.predict.return_value = return_value

        optimal_statistical_geometry_finder._models = {
            "qubit": {
                "fQ": {
                    "pad_gap": mock_model,
                    "pad_height": mock_model,
                }
            },
            "resonator": None,
        }
        component = "qubit"
        target_parameter = "fQ"
        target_parameter_value = 0.1
        geometries = optimal_statistical_geometry_finder.find_optimal_geometry(
            component, target_parameter, target_parameter_value
        )
        assert geometries == {
            "pad_gap": "10.0um",
            "pad_height": "10.0um",
        }

    def test_find_optimal_geometry2(self):
        # Test when target_parameter is not in the model
        from src.optimal_geometry_finder.statistical_model.optimal_geometry_finder import (
            OptimalGeometryFinder as OptimalStatisticalGeometryFinder,
        )

        class OptimalStatisticalGeometryFinderMock(OptimalStatisticalGeometryFinder):
            def __init__(self):
                pass

        optimal_statistical_geometry_finder = OptimalStatisticalGeometryFinderMock()
        optimal_statistical_geometry_finder._models = {
            "qubit": {
                "fQ": {
                    "pad_gap": "model",
                    "pad_height": "model",
                }
            },
            "resonator": None,
        }
        component = "qubit"
        target_parameter = "EC/EJ"
        target_parameter_value = 0.1
        geometries = optimal_statistical_geometry_finder.find_optimal_geometry(
            component, target_parameter, target_parameter_value
        )
        assert geometries == {}
