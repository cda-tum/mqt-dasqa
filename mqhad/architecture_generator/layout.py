class Layout:
    def __init__(self) -> None:
        pass

    def get_layout(
        self, ordered_degree: list[tuple[int, int]], adj_mat: list[list[int, int]]
    ) -> tuple[int, int, list[list[int, int]]]:
        qubit_num = len(ordered_degree)

        assigned_qubit_list = []
        candidate_location = {}
        assigned_location = {}
        # candidate_qubit = []

        qubit_id = ordered_degree[0][0]
        assigned_qubit_list.append([qubit_id, 0, 0])
        ordered_degree.pop(0)
        candidate_location[(0, 1)] = 1
        candidate_location[(1, 0)] = 1
        candidate_location[(-1, 0)] = 1
        candidate_location[(0, -1)] = 1
        assigned_location[(0, 0)] = 1

        for qubit_idx in range(qubit_num - 1):
            candidate_qubit = (0, 0)
            # coupling_strength = 0
            for qubit in ordered_degree:
                qubit_id = qubit[0]
                for assigned_qubit in assigned_qubit_list:
                    assigned_qubit_id = assigned_qubit[0]
                    if adj_mat[qubit_id][assigned_qubit_id] > 0:
                        if qubit[1] > candidate_qubit[1]:
                            candidate_qubit = qubit
                        # 	coupling_strength = qubit[1]

            ordered_degree.remove(candidate_qubit)
            # print(ordered_degree)
            # print(candidate_qubit)

            # Manhattan distance for cost computation
            candidate_location_cost = 1000000000
            selected_location = 0
            for location in candidate_location.keys():
                cost = 0
                for assigned_qubit in assigned_qubit_list:
                    assigned_qubit_id = assigned_qubit[0]
                    if adj_mat[candidate_qubit[0]][assigned_qubit_id] > 0:
                        # 			print(candidate_qubit, assigned_qubit_id)
                        # 					print(adj_mat[candidate_qubit[0]][assigned_qubit_id])
                        # 					print(location)
                        cost += adj_mat[candidate_qubit[0]][assigned_qubit_id] * (
                            abs(location[0] - assigned_qubit[1])
                            + abs(location[1] - assigned_qubit[2])
                        )
                    # TODO: Why need the following line? Is it for non-zero distance but small distance for not connected qubit
                    cost += 0.01 * (
                        abs(location[0] - assigned_qubit[1])
                        + abs(location[1] - assigned_qubit[2])
                    )
                # 			print(cost, location)
                # 			print(candidate_location_cost)
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

        # 	print(assigned_qubit_list)

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

        # TODO: For recentering to "0" later on?
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
        # 	print(qubitgrid)

        return dimX, dimY, qubitgrid
