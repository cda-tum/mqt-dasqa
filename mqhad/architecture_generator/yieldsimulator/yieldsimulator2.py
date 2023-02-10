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
        self, qubit_num: int, edge_list: list[list[tuple[int, int]]]
    ) -> np.ndarray:
        """Generate mask for qubit frequency

        Returns:
            np.array: mask for qubit frequency
        """
        self._summation_mask = getattr(self, "_summation_mask", None)
        if self._summation_mask is not None:
            return self._summation_mask

        arr = []
        max_len = 0
        for qubit, edges in enumerate(edge_list):
            if len(edges) == 1:
                continue

            comb = list(combinations(edges, 2))
            len_comb = len(comb)
            if len_comb > max_len:
                max_len = len_comb
            mask_index_per_qubit = np.column_stack(
                [np.arange(len_comb), qubit * np.ones(len_comb, dtype=int), comb]
            )
            arr.append(mask_index_per_qubit)

        mask_index = np.vstack(arr)
        mask = np.zeros((max_len, qubit_num, qubit_num))
        mask[
            mask_index[:, 0, np.newaxis],
            mask_index[:, 1, np.newaxis],
            mask_index[:, 2:4],
        ] = 1
        self._summation_mask = np.transpose(mask, axes=(0, 2, 1))

        return self._summation_mask
