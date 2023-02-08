from mqhad.architecture_generator.yieldsimulator import YieldSimulator
from mqhad.architecture_generator.chip import ChipInfo
import numpy as np
import pytest


class TestYieldSimulator:
    def test_simulate(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = np.arange(5.0, 5.0 + 0.7 * qubit_num, 0.7)
        sigma = 0.03
        num_trials = 5
        yield_sim = YieldSimulator(chip, frequency_config, qubit_num, sigma, num_trials)
        collision_num, yield_rate = yield_sim.simulate()
        assert collision_num == 0.0
        assert yield_rate == 1.0

    @pytest.mark.slow
    def test_simulate_slow(self):
        chip = ChipInfo()
        chip.load_from_file("mqhad/tests/test_chip/20q_bus4.chip")
        chip.generate_buses()
        qubit_num = 20
        sigma = 0.03
        frequency_config = np.arange(5.0, 5.0 + 0.7 * qubit_num, 0.7)
        num_trials = 2
        yied_sim = YieldSimulator(chip, frequency_config, qubit_num, sigma, num_trials)
        collision_num, yield_rate = yied_sim.simulate()
        assert pytest.approx(collision_num, 0.1) == 55.762
        assert pytest.approx(yield_rate, 0.1) == 0.0
