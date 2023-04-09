from unittest.mock import MagicMock
from mqhad.optimal_geometry_finder.statistical_model.optimal_geometry_finder import (
    OptimalGeometryFinder as OptimalStatisticalGeometryFinder,
)


class TestOptimalStatisticalGeometryFinder:
    def test_find_optimal_geometry(self):
        optimal_statistical_geometry_finder = OptimalStatisticalGeometryFinder()
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
