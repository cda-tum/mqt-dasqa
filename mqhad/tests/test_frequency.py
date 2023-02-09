import numpy as np
from mqhad.architecture_generator.frequency import Frequency


class TestFrequency:
    def test_freq_allocation(self):
        qubit_num = 5
        dimX = 3
        dimY = 3
        qubit_grid = [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]]
        bus_location = [[2, 2]]
        frequency_lowerbound = 5.0
        frequency_upperbound = 5.34
        frequency_step = 0.01
        sigma = 0.03
        frequency = Frequency(
            qubit_num,
            dimX,
            dimY,
            qubit_grid,
            bus_location,
            frequency_lowerbound,
            frequency_upperbound,
            frequency_step,
            sigma,
        )
        freq_qubit_list = frequency.get_frequency_allocation()
        np.testing.assert_allclose(
            freq_qubit_list,
            [
                5.059999999999999,
                5.249999999999995,
                5.0699999999999985,
                5.269999999999994,
                5.17,
            ],
            rtol=1e-2,
        )
