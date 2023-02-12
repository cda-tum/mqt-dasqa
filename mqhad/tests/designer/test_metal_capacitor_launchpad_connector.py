from unittest.mock import patch
import numpy as np


class TestCapacitorLaunchpadConnector:
    def test_generate_capacitor_launchpad_connection(self):
        with patch(
            "qiskit_metal.qlibrary.tlines.pathfinder.RoutePathfinder"
        ) as mock_class:
            from mqhad.designer.capacitor_launchpad_connector.metal import (
                CapacitorLaunchpadConnector,
            )

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
            capacitor_launchpad_connector = CapacitorLaunchpadConnector(
                qubit_grid=qubit_grid
            )
            capacitor_launchpad_connections = (
                capacitor_launchpad_connector.generate_capacitor_launchpad_connection()
            )
            assert len(capacitor_launchpad_connections) == 27

    def test_get_configuration(self):
        pass
