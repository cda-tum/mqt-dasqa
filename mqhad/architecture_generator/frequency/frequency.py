from collections import deque
import numpy as np
from mqhad.architecture_generator.chip import Chip
from mqhad.architecture_generator.yieldsimulator import YieldSimulator


class Frequency:
    def __init__(
        self,
        qubit_num: int,
        dimX: int,
        dimY: int,
        qubit_grid: np.ndarray,
        bus_location: np.ndarray,
        frequency_lowerbound: float,
        frequency_upperbound: float,
        frequency_step: int,
        sigma: float,
    ):
        self.qubit_num = qubit_num
        self.dimX = dimX
        self.dimY = dimY
        self.qubit_grid = qubit_grid
        self.bus_location = bus_location
        self.frequency_lowerbound = frequency_lowerbound
        self.frequency_upperbound = frequency_upperbound
        self.frequency_step = frequency_step
        self.sigma = sigma

    def get_frequency_allocation(
        self,
    ):
        freq_qubit_list = [0.0] * self.qubit_num

        full_chip = self._create_temp_chip(
            self.qubit_num, self.qubit_grid, self.bus_location
        )
        full_adj_mat = full_chip.adjacency_matrix

        center_X = int(self.dimX / 2)
        center_Y = int(self.dimY / 2)

        # print(center_X, center_Y)
        freq_qubit_list[self.qubit_grid[center_X][center_Y]] = (
            self.frequency_lowerbound + self.frequency_upperbound
        ) / 2
        allocated_qubit_num = 1

        is_processed_list = [0] * self.qubit_num
        is_processed_list[self.qubit_grid[center_X][center_Y]] = 1

        bfs_queue = deque()

        qubit_id = self.qubit_grid[center_X][center_Y]
        for next_qubit_id in range(self.qubit_num):
            if (
                full_adj_mat[qubit_id][next_qubit_id] == 1
                and is_processed_list[next_qubit_id] == 0
            ):
                is_processed_list[next_qubit_id] = 1
                bfs_queue.append(next_qubit_id)

        allocated_qubit_list = []
        allocated_qubit_list.append((qubit_id, center_X, center_Y))

        qubit_location_list = self._create_qubit_location(
            self.qubit_num, self.dimX, self.dimY, self.qubit_grid
        )

        while allocated_qubit_num < self.qubit_num:
            allocate_qubit_id = bfs_queue.popleft()
            allocated_qubit_num += 1
            allocated_qubit_list.append(
                (
                    allocate_qubit_id,
                    qubit_location_list[allocate_qubit_id][0],
                    qubit_location_list[allocate_qubit_id][1],
                )
            )

            sub_grid, sub_bus = self._create_sub_grid(
                allocated_qubit_num,
                allocated_qubit_list,
                self.qubit_grid,
                self.bus_location,
            )

            temp_chip = self._create_temp_chip(allocated_qubit_num, sub_grid, sub_bus)
            optimal_freq = self.frequency_lowerbound
            test_freq = self.frequency_lowerbound
            optimal_yield_rate = 0.0

            while test_freq < self.frequency_upperbound:
                temp_freq_config = [0] * allocated_qubit_num
                for idx in range(allocated_qubit_num):
                    temp_freq_config[idx] = freq_qubit_list[
                        allocated_qubit_list[idx][0]
                    ]
                temp_freq_config[-1] = test_freq

                yieldsim = YieldSimulator(
                    temp_chip, temp_freq_config, allocated_qubit_num, self.sigma
                )
                collision_num, yield_rate = yieldsim.simulate()
                if yield_rate > optimal_yield_rate:
                    optimal_yield_rate = yield_rate
                    optimal_freq = test_freq
                test_freq += self.frequency_step

            freq_qubit_list[allocate_qubit_id] = optimal_freq

            for next_qubit_id in range(self.qubit_num):
                if (
                    full_adj_mat[allocate_qubit_id][next_qubit_id] == 1
                    and is_processed_list[next_qubit_id] == 0
                ):
                    is_processed_list[next_qubit_id] = 1
                    bfs_queue.append(next_qubit_id)

        return freq_qubit_list

    def _create_temp_chip(self, qubit_num, qubit_grid, bus_location):
        chip = Chip(qubit_num, qubit_grid, bus_location)
        chip.generate_buses()
        return chip

    def _create_sub_grid(
        self, allocated_qubit_num, allocated_qubit_list, qubit_grid, bus_location
    ):
        minX = 10000
        maxX = 0
        minY = 10000
        maxY = 0

        for idx in range(allocated_qubit_num):
            if minX > allocated_qubit_list[idx][1]:
                minX = allocated_qubit_list[idx][1]
            if maxX < allocated_qubit_list[idx][1]:
                maxX = allocated_qubit_list[idx][1]
            if minY > allocated_qubit_list[idx][2]:
                minY = allocated_qubit_list[idx][2]
            if maxY < allocated_qubit_list[idx][2]:
                maxY = allocated_qubit_list[idx][2]

        dimX = maxX - minX + 1
        dimY = maxY - minY + 1

        sub_grid = [0] * dimX
        for x in range(dimX):
            sub_grid[x] = [-1] * dimY

        # 	reverse = [] * allocated_qubit_num

        for idx in range(allocated_qubit_num):
            sub_grid[allocated_qubit_list[idx][1] - minX][
                allocated_qubit_list[idx][2] - minY
            ] = idx  # allocated_qubit_list[idx][0]
        sub_bus = []
        # 	print('aa', bus_location)
        # 	print(minX, maxX, minY, maxY)
        for bus in bus_location:
            if bus[0] > minX and bus[0] <= maxX and bus[1] > minY and bus[1] <= maxY:
                sub_bus.append((bus[0] - minX, bus[1] - minY))

        return sub_grid, sub_bus

    def _create_qubit_location(self, qubit_num, dimX, dimY, qubit_grid):
        qubit_location_list = [0] * qubit_num
        for x in range(dimX):
            for y in range(dimY):
                if qubit_grid[x][y] > -1:
                    qubit_location_list[qubit_grid[x][y]] = (x, y)
        return qubit_location_list
