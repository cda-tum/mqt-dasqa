import numpy as np


class ChipInfo:
    def __init__(
        self,
        qubit_num: int = 0,
        qubit_grid: np.ndarray = np.array([]),
        cross_bus_list: np.ndarray = [],
    ):
        self.qubit_num = qubit_num
        self.qubit_grid = qubit_grid
        self.cross_bus_list = cross_bus_list
        self._coupling_list = []
        self._grid_edge_list = []
        self._via_edge_list = []
        self._edge_list = []

    @property
    def adjacency_matrix(self):
        return self._adj_mat

    @property
    def coupling_list(self):
        return np.array(self._coupling_list)

    @coupling_list.setter
    def coupling_list(self, coupling_list):
        self._coupling_list = coupling_list

    @property
    def grid_edge_list(self):
        return np.array(self._grid_edge_list)

    @grid_edge_list.setter
    def grid_edge_list(self, grid_edge_list):
        self._grid_edge_list = grid_edge_list

    @property
    def via_edge_list(self):
        return np.array(self._via_edge_list)

    @via_edge_list.setter
    def via_edge_list(self, via_edge_list):
        self._via_edge_list = via_edge_list

    @property
    def edge_list(self):
        return np.array(self._edge_list)

    @edge_list.setter
    def edge_list(self, edge_list):
        self._edge_list = edge_list

    def generate_buses(self):
        self.generate_from_all_2q_bus()
        self.patch_4q_bus()

    def generate_from_all_2q_bus(self):
        dimX = len(self.qubit_grid)
        dimY = len(self.qubit_grid[0])

        self._adj_mat = np.zeros((self.qubit_num, self.qubit_num), dtype=int)

        for x in range(dimX):
            for y in range(dimY):
                if self.qubit_grid[x][y] > -1:
                    if x > 0 and self.qubit_grid[x - 1][y] > -1:
                        self._adj_mat[self.qubit_grid[x][y]][
                            self.qubit_grid[x - 1][y]
                        ] = 1
                        self._adj_mat[self.qubit_grid[x - 1][y]][
                            self.qubit_grid[x][y]
                        ] = 1
                        self._coupling_list.append(
                            [self.qubit_grid[x - 1][y], self.qubit_grid[x][y]]
                        )

                    if y > 0 and self.qubit_grid[x][y - 1] > -1:
                        self._adj_mat[self.qubit_grid[x][y]][
                            self.qubit_grid[x][y - 1]
                        ] = 1
                        self._adj_mat[self.qubit_grid[x][y - 1]][
                            self.qubit_grid[x][y]
                        ] = 1
                        self._coupling_list.append(
                            [self.qubit_grid[x][y - 1], self.qubit_grid[x][y]]
                        )

        self.grid_edge_list = self._coupling_list

        for x in range(1, dimX - 1):
            for y in range(dimY):
                if (
                    self.qubit_grid[x][y] > -1
                    and self.qubit_grid[x - 1][y] > -1
                    and self.qubit_grid[x + 1][y] > -1
                ):
                    self._via_edge_list.append(
                        [
                            self.qubit_grid[x - 1][y],
                            self.qubit_grid[x][y],
                            self.qubit_grid[x + 1][y],
                        ]
                    )
        for x in range(dimX):
            for y in range(1, dimY - 1):
                if (
                    self.qubit_grid[x][y] > -1
                    and self.qubit_grid[x][y - 1] > -1
                    and self.qubit_grid[x][y + 1] > -1
                ):
                    self._via_edge_list.append(
                        [
                            self.qubit_grid[x][y - 1],
                            self.qubit_grid[x][y],
                            self.qubit_grid[x][y + 1],
                        ]
                    )

        self.edge_list = [0] * self.qubit_num
        for qubit_id in range(self.qubit_num):
            self._edge_list[qubit_id] = []

        for coupling in self._coupling_list:
            qubit_i = coupling[0]
            qubit_j = coupling[1]
            self._edge_list[qubit_i].append(qubit_j)
            self._edge_list[qubit_j].append(qubit_i)

    def patch_4q_bus(self):
        for bus in self.cross_bus_list:
            x = bus[0]
            y = bus[1]
            if x > 0 and y > 0:
                if self.qubit_grid[x][y] > -1 and self.qubit_grid[x - 1][y - 1] > -1:
                    qubit_i, qubit_j = (
                        self.qubit_grid[x][y],
                        self.qubit_grid[x - 1][y - 1],
                    )
                    self._adj_mat[qubit_i][qubit_j] = 1
                    self._adj_mat[qubit_j][qubit_i] = 1
                    self._coupling_list.append([qubit_i, qubit_j])
                    self._edge_list[qubit_i].append(qubit_j)
                    self._edge_list[qubit_j].append(qubit_i)

                if self.qubit_grid[x - 1][y] > -1 and self.qubit_grid[x][y - 1] > -1:
                    qubit_i, qubit_j = (
                        self.qubit_grid[x - 1][y],
                        self.qubit_grid[x][y - 1],
                    )
                    self._adj_mat[qubit_i][qubit_j] = 1
                    self._adj_mat[qubit_j][qubit_i] = 1
                    self._coupling_list.append([qubit_i, qubit_j])
                    self._edge_list[qubit_i].append(qubit_j)
                    self._edge_list[qubit_j].append(qubit_i)

    def load_from_file(self, filename):
        fid = open(filename, "r")
        flines = fid.readlines()

        qubit_id = 0
        for line in flines:
            line = line.split()

            if len(line) == 0:
                continue

            if line[0] == "qubit":
                self.qubit_num = int(line[1])

            if line[0] == "griddim":
                dimX = int(line[1])
                dimY = int(line[2])
                self.qubit_grid = [0] * dimX
                for x in range(dimX):
                    self.qubit_grid[x] = [-1] * dimY

            if line[0] == "q":
                x = int(line[1])
                y = int(line[2])
                self.qubit_grid[x][y] = qubit_id
                qubit_id += 1

            if line[0] == "bustype":
                bustype = int(line[1])
                if bustype == 2:
                    self.generate_from_all_2q_bus()
                if bustype == 4:
                    self.generate_from_all_2q_bus()

            if line[0] == "b":
                x = int(line[1])
                y = int(line[2])
                self.cross_bus_list.append([x, y])
        self.patch_4q_bus()
        return
