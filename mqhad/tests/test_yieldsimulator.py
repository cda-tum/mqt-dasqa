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
        yield_sim = YieldSimulator(
            chip, frequency_config, qubit_num, sigma, num_trials=num_trials
        )
        collision_num, yield_rate = yield_sim.simulate()
        assert collision_num == 2.0
        assert yield_rate == 0.0

    # Write test cases for _get_type_1_2_3_collision
    def test_get_type_1_2_3_collision(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = np.arange(5.0, 5.0 + 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )

        yield_success = 1
        frequency_list = [5.000008, 5.000012, 5.000016]
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_1_2_3_collision(
            chip, yield_success, frequency_list, collision_num, collision_stat
        )
        assert collision_num == 8
        assert yield_success == 0
        np.testing.assert_array_equal(collision_stat, [2, 2, 2, 0, 0, 0, 0])

    def test_get_type_4_collision(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = np.arange(5.0, 5.0 + 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )

        yield_success = 1
        frequency_list = [5.000008, 5.000012, 5.000016]
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_4_collision(
            chip, yield_success, frequency_list, collision_num, collision_stat
        )
        assert collision_num == 2
        assert yield_success == 0
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 2, 0, 0, 0])

    # Write test cases for _get_type_5_6_collision
    def test_get_type_5_6_collision(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = np.arange(5.0, 5.0 + 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )

        yield_success = 1
        frequency_list = np.arange(5.000008, 5.000008 + 0.000004 * qubit_num, 0.000004)
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_5_6_collision(
            chip, yield_success, frequency_list, collision_num, collision_stat
        )
        assert collision_num == 18
        assert yield_success == 0
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 0, 6, 6, 0])

    # @pytest.mark.slow
    def test_simulate_slow(self):
        chip = ChipInfo()
        chip.load_from_file("mqhad/tests/test_chip/20q_bus4.chip")
        chip.generate_buses()
        qubit_num = 20
        sigma = 0.03
        frequency_config = np.arange(5.0, 5.0 + 0.7 * qubit_num, 0.7)
        num_trials = 100000
        yied_sim = YieldSimulator(
            chip, frequency_config, qubit_num, sigma, num_trials=num_trials
        )
        collision_num, yield_rate = yied_sim.simulate()
        assert pytest.approx(collision_num, 0.1) == 55.762
        assert pytest.approx(yield_rate, 0.1) == 0.0
