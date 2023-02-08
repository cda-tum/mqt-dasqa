import random
import numpy as np
from mqhad.architecture_generator.chip import ChipInfo


class YieldSimulator:
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
        random.seed(a=0, version=2)

    def simulate(self) -> tuple[float, float]:
        collision_num_list = [0] * self.num_trials
        yield_list = [0] * self.num_trials
        collision_stat_sum = [0] * 7

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
        frequency_list = [0] * qubit_num
        for qubit_id in range(qubit_num):
            frequency_list[qubit_id] = random.gauss(frequency_config[qubit_id], sigma)

        yield_success = 1
        collision_num = 0
        collision_stat = [0] * 7

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

        for grid_edge in chip_info.grid_edge_list:
            qubit_j = grid_edge[0]
            qubit_k = grid_edge[1]

            # Type 4
            if abs(frequency_list[qubit_j] - frequency_list[qubit_k]) > self.delta:
                yield_success = 0
                collision_num += 1
                collision_stat[3] += 1

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

        return collision_num, yield_success, collision_stat
