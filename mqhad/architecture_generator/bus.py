class Bus:
    def __init
    def bus_select(dimX, dimY, qubit_grid, adj_mat, num_4Q_bus):
        bus_locations_4Q = []

        bus_grid = [0] * (dimX - 1)
        for x in range(dimX - 1):
            bus_grid[x] = [0] * (dimY - 1)
        
        bus_weight = [0] * (dimX - 1)
        for x in range(dimX - 1):
            bus_weight[x] = [0] * (dimY - 1)
        
        filtered_weight = [0] * (dimX - 1)
        for x in range(dimX - 1):
            filtered_weight[x] = [0] * (dimY - 1)

        # Sum of weights across diagonals of qubits
        # For the example in Figure 7 (c), the cross-coupling weight of the green square is the 
        # coupling strength of q0,q3 plus that of q1,q2.
        for x in range(dimX - 1):
            for y in range(dimY - 1):
                weight = 0
                if (qubit_grid[x][y] != -1) and (qubit_grid[x + 1][y + 1] != -1):
                    weight += adj_mat[qubit_grid[x][y]][qubit_grid[x + 1][y + 1]]
                if (qubit_grid[x][y + 1] != -1) and (qubit_grid[x + 1][y] != -1):
                    weight += adj_mat[qubit_grid[x][y + 1]][qubit_grid[x + 1][y]]
                bus_weight[x][y] = weight
    #	print(bus_weight)

        while (num_4Q_bus > 0):
            # However, the cross-coupling weight is not accurate enough 
            # to evaluate the benefit of 4-qubit for a square because the prohibited condition is not yet considered. 
            for x in range(dimX - 1):
                for y in range(dimY - 1):
                    weight = bus_weight[x][y]
                    if x != 0:
                        weight -= bus_weight[x - 1][y]
                    if y != 0:
                        weight -= bus_weight[x][y - 1]
                    if y != (dimY - 2):
                        weight -= bus_weight[x][y + 1]
                    if x != (dimX - 2):
                        weight -= bus_weight[x + 1][y]
                    filtered_weight[x][y] = weight
            
            # After applying the filter, we will select one square with the highest filtered weight.
            select_X = -1
            select_Y = -1
            select_weight = -100000000
            for x in range(dimX - 1):
                for y in range(dimY - 1):
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

            bus_locations_4Q.append((select_X+1, select_Y+1))
            bus_grid[select_X][select_Y] = 1

            # We also change their weights to zero because they should not affect the 4-qubit selection among the remaining squares.
            bus_weight[select_X][select_Y] = 0
            if select_X != 0:
                bus_weight[select_X - 1][select_Y] = 0
            if select_X != (dimX - 2):
                bus_weight[select_X + 1][select_Y] = 0
            if select_Y != 0:
                bus_weight[select_X][select_Y - 1] = 0
            if select_Y != (dimY - 2):
                bus_weight[select_X][select_Y + 1] = 0
    #print(filtered_weight)

            

            num_4Q_bus -= 1

        return bus_grid, bus_locations_4Q