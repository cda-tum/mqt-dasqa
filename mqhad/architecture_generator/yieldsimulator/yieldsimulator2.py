import random
from itertools import combinations
from collections import OrderedDict
import numpy as np
from .yieldsimulator_base import YieldSimulatorBase
from mqhad.architecture_generator.chip import ChipInfo

random.seed(a=0, version=2)


class YieldSimulator2(YieldSimulatorBase):
    def __init__(
        self,
        chip_info: ChipInfo,
        frequency_config: np.ndarray,
        qubit_num: int,
        sigma: float = 0.00,
        delta: float = 0.34,
        num_trials: int = 100000,
    ) -> None:
        self.chip_info = chip_info
        self.qubit_num = qubit_num
        self.sigma = sigma
        self.frequency_config = frequency_config
        self.delta = delta
        self.num_trials = num_trials

    def reset_seed(self, seed: int = 0) -> None:
        """Reset the seed of random number generator.

        Args:
            seed (int, optional): Seed. Defaults to 0.
        """
        random.seed(a=seed, version=2)

    def simulate(self) -> tuple[float, float]:
        collision_num_list = np.zeros(self.num_trials, dtype=int)
        yield_list = np.zeros(self.num_trials, dtype=int)
        collision_stat_sum = np.zeros(7, dtype=int)

        for trial_id in range(self.num_trials):
            (
                collision_num_list[trial_id],
                yield_list[trial_id],
                collision_stat,
            ) = self._one_trial_sim(
                self.qubit_num, self.chip_info, self.sigma, self.frequency_config
            )
            for i in range(7):
                collision_stat_sum[i] += collision_stat[i]

        collision_num = float(sum(collision_num_list)) / float(self.num_trials)
        yield_rate = float(sum(yield_list)) / float(self.num_trials)

        return collision_num, yield_rate

    def _one_trial_sim(
        self,
        qubit_num: int,
        chip_info: ChipInfo,
        sigma: float,
        frequency_config: np.ndarray,
    ) -> tuple[int, int, list[int]]:
        frequency_list = np.zeros(qubit_num)
        for qubit_id in range(qubit_num):
            frequency_list[qubit_id] = random.gauss(frequency_config[qubit_id], sigma)

        yield_success = 1
        collision_num = 0
        collision_stat = np.zeros(7)

        yield_success, collision_num, collision_stat = self._get_type_1_2_3_collision(
            chip_info, yield_success, frequency_list, collision_num, collision_stat
        )

        yield_success, collision_num, collision_stat = self._get_type_4_collision(
            chip_info, yield_success, frequency_list, collision_num, collision_stat
        )

        yield_success, collision_num, collision_stat = self._get_type_5_6_collision(
            chip_info,
            yield_success,
            frequency_list,
            collision_num,
            collision_stat,
        )

        yield_success, collision_num, collision_stat = self._get_type_7_collision(
            qubit_num,
            chip_info,
            yield_success,
            frequency_list,
            collision_num,
            collision_stat,
        )

        return collision_num, yield_success, collision_stat

    def _get_type_1_2_3_collision(
        self,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: np.ndarray,
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        coupling = chip_info.coupling_list

        if len(coupling) == 0:
            return yield_success, collision_num, collision_stat

        coupling_freq_delta = np.abs(
            frequency_list[coupling[:, 0]] - frequency_list[coupling[:, 1]]
        )

        # Type 1
        mask = coupling_freq_delta < 0.017
        collision_num += np.sum(2 * mask)
        collision_stat[0] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success

        # Type 2
        mask = np.abs(coupling_freq_delta - (self.delta / 2)) < 0.004
        collision_num += np.sum(mask)
        collision_stat[1] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success

        # Type 3
        mask = np.abs(coupling_freq_delta - self.delta) < 0.025
        collision_num += np.sum(mask)
        collision_stat[2] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success

        return yield_success, collision_num, collision_stat

    def _get_type_4_collision(
        self,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: list[float],
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        grid_edge = chip_info.grid_edge_list

        if len(grid_edge) == 0:
            return yield_success, collision_num, collision_stat

        grid_freq_edge_delta = np.abs(
            frequency_list[grid_edge[:, 0]] - frequency_list[grid_edge[:, 1]]
        )

        # Type 4
        mask = grid_freq_edge_delta > self.delta
        collision_num += np.sum(mask)
        collision_stat[3] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success

        return yield_success, collision_num, collision_stat

    def _get_type_5_6_collision(
        self,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: np.ndarray,
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        via_edge = chip_info.via_edge_list

        if len(via_edge) == 0:
            return yield_success, collision_num, collision_stat

        via_edge_freq_delta = np.abs(
            frequency_list[via_edge[:, 0]] - frequency_list[via_edge[:, 2]]
        )

        # Type 5
        mask = via_edge_freq_delta < 0.017
        collision_num += np.sum(2 * mask)
        collision_stat[4] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success

        # Type 6
        mask = np.abs(via_edge_freq_delta - self.delta) < 0.025
        collision_num += np.sum(mask)
        collision_stat[5] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success

        return yield_success, collision_num, collision_stat

    def _get_type_7_collision(
        self,
        qubit_num: int,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: np.ndarray,
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        edge_list = chip_info.edge_list

        if len(edge_list) == 0:
            return yield_success, collision_num, collision_stat

        summation_mask = self._get_summation_mask(qubit_num, edge_list)

        frequency_list_delta = 2 * frequency_list - self.delta

        edges_sum = frequency_list @ summation_mask
        mask = np.abs(frequency_list_delta - edges_sum) < 0.017

        collision_num += np.sum(mask)
        collision_stat[6] += np.sum(mask)
        yield_success = 0 if np.any(mask) else yield_success
        return yield_success, collision_num, collision_stat

    def _get_summation_mask(
        self,
        qubit_num: int,
        edge_list: list[list[tuple[int, int]]],
    ):
        """Generate mask for qubit frequency

        Returns:
            np.array: mask for qubit frequency
        """
        self._summation_mask = getattr(self, "_summation_mask", None)
        if self._summation_mask is not None:
            return self._summation_mask

        edges_combinations, max_len = self._generate_combinations(edge_list)
        mask = np.zeros((max_len, qubit_num, qubit_num))

        for qubit, edges in edges_combinations.items():
            if len(edges) == 0:
                continue
            edges_len = len(edges)
            depth_indexes = (
                np.arange(0, 0 + 1 * edges_len, step=1, dtype=int)
                .repeat(2)
                .reshape(edges_len * 2, 1)
            )
            row_indexes = np.array([qubit] * (len(edges) * 2)).reshape(edges_len * 2, 1)
            edge_indexes = np.reshape(edges, (edges_len * 2, 1))
            mask_index = np.concatenate(
                (depth_indexes, row_indexes, edge_indexes), axis=1
            )
            mask[mask_index[:, 0], mask_index[:, 1], mask_index[:, 2]] = 1

        self._summation_mask = np.transpose(mask, axes=(0, 2, 1))

        return self._summation_mask

    def _generate_combinations(
        self,
        edge_list,
    ) -> tuple[OrderedDict[int, list[tuple[int, int]]], int]:
        """Generate combinations for each list in edge_list and store in a dictionary with keys

        Args:
            edge_list (np.array): list of lists of qubit neighbors
        Returns:
            dict: keys are the qubit index and values are the combinations
        """
        combinations_dict = OrderedDict()
        max_len = 0
        for i in range(len(edge_list)):
            combinations_dict[i] = list(combinations(edge_list[i], 2))
            if len(combinations_dict[i]) > max_len:
                max_len = len(combinations_dict[i])
        return combinations_dict, max_len
