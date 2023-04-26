from unittest.mock import patch
from collections import OrderedDict
import numpy as np


class TestRouteMeanderConnector:
    def test_generate_qubit_connection(self):
        with patch("qiskit_metal.qlibrary.tlines.meandered.RouteMeander") as mock_class:
            from src.mapper.qubit_connector.metal import RouteMeanderConnector

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
            qubit_frequencies = np.linspace(5.0, 5.1, 27)
            route_connector = RouteMeanderConnector(
                qubit_grid=qubit_grid, qubit_frequencies=qubit_frequencies
            )
            qubit_connections = route_connector.generate_qubit_connection()
            assert len(qubit_connections) == 28

    def test_get_upward_connection_configuration(self):
        from src.mapper.qubit_connector.metal import RouteMeanderConnector

        route_connector = RouteMeanderConnector()
        assert route_connector._get_upward_connection_configuration(4, 4) == (
            "B0",
            "B2",
            "700um",
        )
        assert route_connector._get_upward_connection_configuration(4, 3) == (
            "B1",
            "B3",
            "-700um",
        )
        assert route_connector._get_upward_connection_configuration(3, 4) == (
            "B1",
            "B3",
            "-700um",
        )
        assert route_connector._get_upward_connection_configuration(3, 3) == (
            "B0",
            "B2",
            "700um",
        )

    def test_sideway_connection_configuration(self):
        from src.mapper.qubit_connector.metal import RouteMeanderConnector

        route_connector = RouteMeanderConnector()
        assert route_connector._get_sideway_connection_configuration(0, 2) == (
            "B1",
            "B0",
            OrderedDict({0: ["R", "150um"]}),
        )
        assert route_connector._get_sideway_connection_configuration(1, 2) == (
            "B3",
            "B2",
            OrderedDict(),
        )
        assert route_connector._get_sideway_connection_configuration(0, 3) == (
            "B3",
            "B2",
            OrderedDict(),
        )
        assert route_connector._get_sideway_connection_configuration(1, 3) == (
            "B1",
            "B0",
            OrderedDict({0: ["R", "150um"]}),
        )

    def test_find_resonator_length(self):
        pass
