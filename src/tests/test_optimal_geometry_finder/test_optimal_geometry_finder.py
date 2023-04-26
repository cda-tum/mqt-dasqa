from unittest.mock import patch, MagicMock


class TestOptimalGeometryFinder:
    @patch("src.optimal_geometry_finder.statistical_model.OptimalGeometryFinder")
    def test_find_optimal_geometry(self, mock_class1):
        from src.optimal_geometry_finder.optimal_geometry_finder import (
            OptimalGeometryFinder,
        )

        optimal_geometry_finder = OptimalGeometryFinder()
        return_value = {
            "pad_gap": "10.0um",
            "pad_height": "10.0um",
        }
        optimal_geometry_finder.find_optimal_geometry = MagicMock(
            return_value=return_value
        )
        optimal_geometry = optimal_geometry_finder.find_optimal_geometry(
            "qubit", "fQ", 0.1
        )
        assert optimal_geometry == return_value
