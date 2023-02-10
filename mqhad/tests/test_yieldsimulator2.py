import time
from collections import OrderedDict
from unittest.mock import MagicMock
from mqhad.architecture_generator.yieldsimulator import YieldSimulator2
from mqhad.architecture_generator.chip import ChipInfo
import numpy as np
import pytest


class TestYieldSimulator2:
    def test_simulate(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        num_trials = 100000

        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, num_trials=num_trials
        )
        yield_sim.reset_seed()

        st = time.time()
        collision_num, yield_rate = yield_sim.simulate()
        et = time.time()
        print("time: ", (et - st) * 1000)
        assert pytest.approx(collision_num, 0.1) == 2.0
        assert yield_rate == 0.0

    def test_get_type_1_2_3_collision_failure(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
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

    def test_get_type_1_2_3_collision_success(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_1_2_3_collision(
            chip, yield_success, frequency_list, collision_num, collision_stat
        )
        assert collision_num == 0
        assert yield_success == 1
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 0, 0, 0, 0])

    def test_get_type_4_collision_failure(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
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

    def test_get_type_4_collision_success(self):
        qubit_num = 3
        qubit_grid = [[0, 1], [-1, 2]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        sigma = 0.03
        delta = 1e-1
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_4_collision(
            chip, yield_success, frequency_list, collision_num, collision_stat
        )
        assert collision_num == 0
        assert yield_success == 1
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 0, 0, 0, 0])

    def test_get_type_5_6_collision_failure(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
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

    def test_get_type_5_6_collision_success(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_5_6_collision(
            chip, yield_success, frequency_list, collision_num, collision_stat
        )
        assert collision_num == 0
        assert yield_success == 1
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 0, 0, 0, 0])

    def test_get_type_7_collision_failure(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        sigma = 0.03
        delta = 1e-6
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.000004 * qubit_num, 0.000004)
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_7_collision(
            qubit_num,
            chip,
            yield_success,
            frequency_list,
            collision_num,
            collision_stat,
        )
        assert collision_num == 22
        assert yield_success == 0
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 0, 0, 0, 22])

    def test_get_type_7_collision_success(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1.0
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        yield_success = 1
        frequency_list = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        collision_num = 0
        collision_stat = np.zeros(7, dtype=int)

        st = time.time()
        (
            yield_success,
            collision_num,
            collision_stat,
        ) = yield_sim._get_type_7_collision(
            qubit_num,
            chip,
            yield_success,
            frequency_list,
            collision_num,
            collision_stat,
        )
        et = time.time()
        print("Execution time: ", (et - st) * 1000)
        assert collision_num == 0
        assert yield_success == 1
        np.testing.assert_array_equal(collision_stat, [0, 0, 0, 0, 0, 0, 0])

    def test_generate_combinations(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1.0
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        edge_list = np.array(
            [
                [1, 3],
                [0, 2, 4],
                [1, 5],
                [0, 4, 6],
                [1, 3, 5, 7],
                [2, 4, 8],
                [3, 7],
                [4, 6, 8],
                [5, 7],
            ],
            dtype=object,
        )
        qubit_combinations, max_len = yield_sim._generate_combinations(edge_list)
        assert qubit_combinations == OrderedDict(
            [
                (0, [(1, 3)]),
                (1, [(0, 2), (0, 4), (2, 4)]),
                (2, [(1, 5)]),
                (3, [(0, 4), (0, 6), (4, 6)]),
                (4, [(1, 3), (1, 5), (1, 7), (3, 5), (3, 7), (5, 7)]),
                (5, [(2, 4), (2, 8), (4, 8)]),
                (6, [(3, 7)]),
                (7, [(4, 6), (4, 8), (6, 8)]),
                (8, [(5, 7)]),
            ]
        )
        assert max_len == 6

    def test_get_summation_mask(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1.0
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        edge_list = np.array(
            [
                [1, 3],
                [0, 2, 4],
                [1, 5],
                [0, 4, 6],
                [1, 3, 5, 7],
                [2, 4, 8],
                [3, 7],
                [4, 6, 8],
                [5, 7],
            ],
            dtype=object,
        )

        yield_sim._generate_combinations = MagicMock()
        yield_sim._generate_combinations.return_value = (
            OrderedDict(
                [
                    (0, [(1, 3)]),
                    (1, [(0, 2), (0, 4), (2, 4)]),
                    (2, [(1, 5)]),
                    (3, [(0, 4), (0, 6), (4, 6)]),
                    (4, [(1, 3), (1, 5), (1, 7), (3, 5), (3, 7), (5, 7)]),
                    (5, [(2, 4), (2, 8), (4, 8)]),
                    (6, [(3, 7)]),
                    (7, [(4, 6), (4, 8), (6, 8)]),
                    (8, [(5, 7)]),
                ]
            ),
            6,
        )

        mask = yield_sim._get_summation_mask(qubit_num, edge_list)
        assert yield_sim._generate_combinations.call_count == 1
        assert yield_sim._summation_mask is not None
        np.testing.assert_array_equal(
            mask,
            [
                [
                    [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                ],
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                ],
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
            ],
        )

    def test_get_summation_mask_assigned(self):
        qubit_num = 9
        qubit_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cross_list_bus = []
        chip = ChipInfo(qubit_num, qubit_grid, cross_list_bus)
        chip.generate_buses()
        frequency_config = 5.0 + np.arange(0.0, 0.7 * qubit_num, 0.7)
        sigma = 0.03
        delta = 1.0
        num_trials = 5
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, delta, num_trials
        )
        yield_sim.reset_seed()

        edge_list = np.array(
            [
                [1, 3],
                [0, 2, 4],
                [1, 5],
                [0, 4, 6],
                [1, 3, 5, 7],
                [2, 4, 8],
                [3, 7],
                [4, 6, 8],
                [5, 7],
            ],
            dtype=object,
        )

        yield_sim._summation_mask = np.array(
            [
                [
                    [0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 0, 1, 1, 1, 1, 1, 1],
                ],
                [
                    [1, 1, 1, 0, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 0, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 0, 1, 1, 1],
                ],
            ]
        )
        mask = yield_sim._get_summation_mask(qubit_num, edge_list)
        np.testing.assert_array_equal(mask, yield_sim._summation_mask)

    @pytest.mark.slow
    def test_simulate_slow(self):
        chip = ChipInfo()
        chip.load_from_file("mqhad/tests/test_chip/20q_bus4.chip")
        qubit_num = 20
        sigma = 0.03
        frequency_config = [
            5.0,
            5.07,
            5.13,
            5.20,
            5.27,
            5.13,
            5.20,
            5.27,
            5.0,
            5.07,
            5.27,
            5.0,
            5.07,
            5.13,
            5.20,
            5.07,
            5.13,
            5.20,
            5.27,
            5.0,
        ]
        num_trials = 100000
        yield_sim = YieldSimulator2(
            chip, frequency_config, qubit_num, sigma, num_trials=num_trials
        )
        yield_sim.reset_seed()

        collision_num, yield_rate = yield_sim.simulate()
        assert pytest.approx(collision_num) == 12.78752
        assert yield_rate == 0.0
