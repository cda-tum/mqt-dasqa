from unittest.mock import patch
import numpy as np


class TestMetalCapacitor:
    def test_generate_capacitor(self):
        with patch(
            "qiskit_metal.qlibrary.lumped.cap_n_interdigital.CapNInterdigital"
        ) as mock_class:
            from mqhad.mapper.capacitor.metal import Capacitor

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
            capacitor = Capacitor(qubit_grid=qubit_grid)
            capacitors = capacitor.generate_capacitor()
            assert len(capacitors) == 27

    def test_get_configuration(self):
        pass
