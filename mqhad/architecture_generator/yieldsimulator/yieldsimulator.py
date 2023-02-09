import random
import numpy as np
from .yieldsimulator_base import YieldSimulatorBase
from mqhad.architecture_generator.chip import ChipInfo

random.seed(a=0, version=2)


class YieldSimulator(YieldSimulatorBase):
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

        # Vectorize this for loop using numpy
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
        frequency_list: list[float],
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        for edge in chip_info.coupling_list:
            qubit_j = edge[0]
            qubit_k = edge[1]

            edge_freq_delta = abs(frequency_list[qubit_j] - frequency_list[qubit_k])

            # Type 1
            if edge_freq_delta < 0.017:
                yield_success = 0
                collision_num += 2
                collision_stat[0] += 1

            # Type 2
            if abs(edge_freq_delta - (self.delta / 2)) < 0.004:
                yield_success = 0
                collision_num += 1
                collision_stat[1] += 1

            # Type 3
            if abs(edge_freq_delta - self.delta) < 0.025:
                yield_success = 0
                collision_num += 1
                collision_stat[2] += 1

        return yield_success, collision_num, collision_stat

    def _get_type_4_collision(
        self,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: list[float],
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        for grid_edge in chip_info.grid_edge_list:
            qubit_j = grid_edge[0]
            qubit_k = grid_edge[1]

            # Type 4
            if abs(frequency_list[qubit_j] - frequency_list[qubit_k]) > self.delta:
                yield_success = 0
                collision_num += 1
                collision_stat[3] += 1
        return yield_success, collision_num, collision_stat

    def _get_type_5_6_collision(
        self,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: list[float],
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        for via_edge in chip_info.via_edge_list:
            qubit_i = via_edge[0]
            qubit_k = via_edge[2]

            via_edge_feq_delta = abs(frequency_list[qubit_i] - frequency_list[qubit_k])

            # Type 5
            if via_edge_feq_delta < 0.017:
                yield_success = 0
                collision_num += 2
                collision_stat[4] += 1

            # Type 6
            if abs(via_edge_feq_delta - self.delta) < 0.025:
                yield_success = 0
                collision_num += 1
                collision_stat[5] += 1
        return yield_success, collision_num, collision_stat

    def _get_type_7_collision(
        self,
        qubit_num: int,
        chip_info: ChipInfo,
        yield_success: int,
        frequency_list: list[float],
        collision_num: int,
        collision_stat: np.ndarray,
    ) -> tuple[int, int, np.ndarray]:
        for qubit_j in range(qubit_num):
            for qubit_i_id in range(len(chip_info.edge_list[qubit_j])):
                qubit_i = chip_info.edge_list[qubit_j][qubit_i_id]
                for qubit_k_id in range(
                    qubit_i_id + 1, len(chip_info.edge_list[qubit_j])
                ):
                    qubit_k = chip_info.edge_list[qubit_j][qubit_k_id]

                    # Type 7
                    if (
                        abs(
                            (2 * frequency_list[qubit_j] - self.delta)
                            - (frequency_list[qubit_k] + frequency_list[qubit_i])
                        )
                        < 0.017
                    ):
                        yield_success = 0
                        collision_num += 1
                        collision_stat[6] += 1
        return yield_success, collision_num, collision_stat
