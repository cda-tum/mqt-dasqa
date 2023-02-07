class Layout:
    def __init__(self) -> None:
        pass

    def get_layout(
        self, ordered_degree: list[tuple[int, int]], adj_mat: list[list[int]]
    ) -> tuple[int, int, list[list[int]]]:
        qubit_num = len(ordered_degree)

        assigned_qubit_list = []
        candidate_location = {}
        assigned_location = {}

        qubit_id = ordered_degree[0][0]
        assigned_qubit_list.append([qubit_id, 0, 0])
        ordered_degree.pop(0)
        candidate_location[(0, 1)] = 1
        candidate_location[(1, 0)] = 1
        candidate_location[(-1, 0)] = 1
        candidate_location[(0, -1)] = 1
        assigned_location[(0, 0)] = 1

        for _ in range(qubit_num - 1):
            candidate_qubit = (0, 0)

            for qubit in ordered_degree:
                qubit_id = qubit[0]
                qubit_coupling_strength = qubit[1]
                for assigned_qubit in assigned_qubit_list:
                    assigned_qubit_id = assigned_qubit[0]
                    if adj_mat[qubit_id][assigned_qubit_id] > 0:
                        candidate_qubit_coupling_strength = candidate_qubit[1]
                        if qubit_coupling_strength > candidate_qubit_coupling_strength:
                            candidate_qubit = qubit

            ordered_degree.remove(candidate_qubit)

            # Manhattan distance for cost computation
            candidate_location_cost = 1000000000
            selected_location = 0
            for location in candidate_location.keys():
                cost = 0
                for assigned_qubit in assigned_qubit_list:
                    cost += self._calculate_distance_to_assigned_qubits(
                        adj_mat, candidate_qubit, assigned_qubit, location
                    )

                if cost < candidate_location_cost:
                    candidate_location_cost = cost
                    selected_location = location

            location = selected_location
            # 		print(location)

            candidate_location.pop(location)
            assigned_qubit_list.append([candidate_qubit[0], location[0], location[1]])
            assigned_location[location] = 1
            new_locations = [
                (location[0], location[1] + 1),
                (location[0] + 1, location[1]),
                (location[0] - 1, location[1]),
                (location[0], location[1] - 1),
            ]
            for location in new_locations:
                if (location in assigned_location) or (location in candidate_location):
                    continue
                candidate_location[location] = 1

        minX, minY, maxX, maxY = self._extract_min_max_XY(assigned_qubit_list)

        dimX, dimY, qubitgrid = self._center_layout(
            assigned_qubit_list, minX, minY, maxX, maxY
        )

        return dimX, dimY, qubitgrid

    def _calculate_distance_to_assigned_qubits(
        self,
        adj_mat: list[list[int]],
        candidate_qubit: tuple[int, int],
        assigned_qubit: tuple[int, int, int],
        location: tuple[int, int],
    ) -> float:
        cost = 0
        assigned_qubit_id = assigned_qubit[0]
        if adj_mat[candidate_qubit[0]][assigned_qubit_id] > 0:
            cost += adj_mat[candidate_qubit[0]][assigned_qubit_id] * (
                abs(location[0] - assigned_qubit[1])
                + abs(location[1] - assigned_qubit[2])
            )
        cost += 0.01 * (
            abs(location[0] - assigned_qubit[1]) + abs(location[1] - assigned_qubit[2])
        )
        return cost

    def _center_layout(
        self,
        assigned_qubit_list: list[list[int]],
        minX: int,
        minY: int,
        maxX: int,
        maxY: int,
    ) -> tuple[int, int, list[list[int]]]:
        offsetX = -minX
        offsetY = -minY

        dimX = maxX - minX + 1
        dimY = maxY - minY + 1
        qubitgrid = [0] * dimX
        for x in range(dimX):
            qubitgrid[x] = [-1] * dimY

        for qubit_info in assigned_qubit_list:
            qubit_info[1] += offsetX
            qubit_info[2] += offsetY
            qubitgrid[qubit_info[1]][qubit_info[2]] = qubit_info[0]
        return dimX, dimY, qubitgrid

    def _extract_min_max_XY(
        self, assigned_qubit_list: list[list[int]]
    ) -> tuple[int, int, int, int]:
        minX = 0
        minY = 0
        maxX = 0
        maxY = 0
        for qubit in assigned_qubit_list:
            if minX > qubit[1]:
                minX = qubit[1]
            if maxX < qubit[1]:
                maxX = qubit[1]
            if minY > qubit[2]:
                minY = qubit[2]
            if maxY < qubit[2]:
                maxY = qubit[2]
        return minX, minY, maxX, maxY
