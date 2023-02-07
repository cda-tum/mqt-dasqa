class Bus:
    def __init__(self, dimX, dimY, qubit_grid, adj_mat, num_4Q_bus):
        self.dimX = dimX
        self.dimY = dimY
        self.qubit_grid = qubit_grid
        self.adj_mat = adj_mat
        self.num_4Q_bus = num_4Q_bus

    def bus_select(self):
        bus_locations_4Q = []

        bus_grid = [0] * (self.dimX - 1)
        for x in range(self.dimX - 1):
            bus_grid[x] = [0] * (self.dimY - 1)

        bus_weight = [0] * (self.dimX - 1)
        for x in range(self.dimX - 1):
            bus_weight[x] = [0] * (self.dimY - 1)

        filtered_weight = [0] * (self.dimX - 1)
        for x in range(self.dimX - 1):
            filtered_weight[x] = [0] * (self.dimY - 1)

        # Sum of weights across diagonals of qubits
        # For the example in Figure 7 (c), the cross-coupling weight of the green square is the
        # coupling strength of q0,q3 plus that of q1,q2.
        for x in range(self.dimX - 1):
            for y in range(self.dimY - 1):
                weight = 0
                if (self.qubit_grid[x][y] != -1) and (
                    self.qubit_grid[x + 1][y + 1] != -1
                ):
                    weight += self.adj_mat[self.qubit_grid[x][y]][
                        self.qubit_grid[x + 1][y + 1]
                    ]
                if (self.qubit_grid[x][y + 1] != -1) and (
                    self.qubit_grid[x + 1][y] != -1
                ):
                    weight += self.adj_mat[self.qubit_grid[x][y + 1]][
                        self.qubit_grid[x + 1][y]
                    ]
                bus_weight[x][y] = weight
        # 	print(bus_weight)

        while self.num_4Q_bus > 0:
            # However, the cross-coupling weight is not accurate enough
            # to evaluate the benefit of 4-qubit for a square because the prohibited condition is not yet considered.
            for x in range(self.dimX - 1):
                for y in range(self.dimY - 1):
                    weight = bus_weight[x][y]
                    if x != 0:
                        weight -= bus_weight[x - 1][y]
                    if y != 0:
                        weight -= bus_weight[x][y - 1]
                    if y != (self.dimY - 2):
                        weight -= bus_weight[x][y + 1]
                    if x != (self.dimX - 2):
                        weight -= bus_weight[x + 1][y]
                    filtered_weight[x][y] = weight

            # After applying the filter, we will select one square with the highest filtered weight.
            select_X = -1
            select_Y = -1
            select_weight = -100000000
            for x in range(self.dimX - 1):
                for y in range(self.dimY - 1):
                    if bus_weight[x][y] > 0:
                        if filtered_weight[x][y] > select_weight:
                            select_X = x
                            select_Y = y
                            select_weight = filtered_weight[x][y]

            # Break if no suitable position anymore for 4-qubit buses.
            # The algorithm will iterate again to select the next square until
            # there are not more squares available or we have already applied enough number of 4-qubit buses.
            if select_X == -1:
                break

            bus_locations_4Q.append((select_X + 1, select_Y + 1))
            bus_grid[select_X][select_Y] = 1

            # We also change their weights to zero because they should not affect the 4-qubit selection among the remaining squares.
            bus_weight[select_X][select_Y] = 0
            if select_X != 0:
                bus_weight[select_X - 1][select_Y] = 0
            if select_X != (self.dimX - 2):
                bus_weight[select_X + 1][select_Y] = 0
            if select_Y != 0:
                bus_weight[select_X][select_Y - 1] = 0
            if select_Y != (self.dimY - 2):
                bus_weight[select_X][select_Y + 1] = 0
            # print(filtered_weight)

            self.num_4Q_bus -= 1

        return bus_grid, bus_locations_4Q
