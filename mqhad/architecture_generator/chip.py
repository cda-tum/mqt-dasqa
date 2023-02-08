class ChipInfo:
    def __init__(self):
        self.qubit_num = 0
        self.coupling_list = []
        self.grid_edge_list = []
        self.via_edge_list = []
        self.edge_list = []
        self.qubitgrid = []
        self.adj_mat = []
        self.crossbuslist = []

    def displayinfo(self):
        print(self.qubit_num)
        print(self.coupling_list)
        print(self.grid_edge_list)
        print(self.via_edge_list)
        print(self.edge_list)
        print(self.qubitgrid)
        print(self.adj_mat)
        print(self.crossbuslist)

    def generatefromAll2QBus(self):
        dimX = len(self.qubitgrid)
        dimY = len(self.qubitgrid[0])

        self.adj_mat = [0] * self.qubit_num
        for qubit_id in range(self.qubit_num):
            self.adj_mat[qubit_id] = [0] * self.qubit_num

        for x in range(dimX):
            for y in range(dimY):
                if self.qubitgrid[x][y] > -1:
                    if x > 0 and self.qubitgrid[x - 1][y] > -1:
                        self.adj_mat[self.qubitgrid[x][y]][self.qubitgrid[x - 1][y]] = 1
                        self.adj_mat[self.qubitgrid[x - 1][y]][self.qubitgrid[x][y]] = 1
                        self.coupling_list.append(
                            [self.qubitgrid[x - 1][y], self.qubitgrid[x][y]]
                        )

                    if y > 0 and self.qubitgrid[x][y - 1] > -1:
                        self.adj_mat[self.qubitgrid[x][y]][self.qubitgrid[x][y - 1]] = 1
                        self.adj_mat[self.qubitgrid[x][y - 1]][self.qubitgrid[x][y]] = 1
                        self.coupling_list.append(
                            [self.qubitgrid[x][y - 1], self.qubitgrid[x][y]]
                        )

        self.grid_edge_list = self.coupling_list

        # 		print('vai')

        for x in range(1, dimX - 1):
            for y in range(dimY):
                # 				print(self.qubitgrid[x][y], self.qubitgrid[x][y-1], self.qubitgrid[x][y+1])
                if (
                    self.qubitgrid[x][y] > -1
                    and self.qubitgrid[x - 1][y] > -1
                    and self.qubitgrid[x + 1][y] > -1
                ):
                    self.via_edge_list.append(
                        [
                            self.qubitgrid[x - 1][y],
                            self.qubitgrid[x][y],
                            self.qubitgrid[x + 1][y],
                        ]
                    )
        for x in range(dimX):
            for y in range(1, dimY - 1):
                if (
                    self.qubitgrid[x][y] > -1
                    and self.qubitgrid[x][y - 1] > -1
                    and self.qubitgrid[x][y + 1] > -1
                ):
                    self.via_edge_list.append(
                        [
                            self.qubitgrid[x][y - 1],
                            self.qubitgrid[x][y],
                            self.qubitgrid[x][y + 1],
                        ]
                    )

        self.edge_list = [0] * self.qubit_num
        for qubit_id in range(self.qubit_num):
            self.edge_list[qubit_id] = []

        # 		print(self.edge_list)

        for coupling in self.coupling_list:
            qubit_i = coupling[0]
            qubit_j = coupling[1]
            self.edge_list[qubit_i].append(qubit_j)
            self.edge_list[qubit_j].append(qubit_i)

    def Patch4QBus(self):
        for bus in self.crossbuslist:
            x = bus[0]
            y = bus[1]
            if x > 0 and y > 0:
                if self.qubitgrid[x][y] > -1 and self.qubitgrid[x - 1][y - 1] > -1:
                    qubit_i, qubit_j = (
                        self.qubitgrid[x][y],
                        self.qubitgrid[x - 1][y - 1],
                    )
                    self.adj_mat[qubit_i][qubit_j] = 1
                    self.adj_mat[qubit_j][qubit_i] = 1
                    self.coupling_list.append([qubit_i, qubit_j])
                    self.edge_list[qubit_i].append(qubit_j)
                    self.edge_list[qubit_j].append(qubit_i)

                if self.qubitgrid[x - 1][y] > -1 and self.qubitgrid[x][y - 1] > -1:
                    qubit_i, qubit_j = (
                        self.qubitgrid[x - 1][y],
                        self.qubitgrid[x][y - 1],
                    )
                    self.adj_mat[qubit_i][qubit_j] = 1
                    self.adj_mat[qubit_j][qubit_i] = 1
                    self.coupling_list.append([qubit_i, qubit_j])
                    self.edge_list[qubit_i].append(qubit_j)
                    self.edge_list[qubit_j].append(qubit_i)

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
                # self.qubitgrid = []
                dimX = int(line[1])
                dimY = int(line[2])
                self.qubitgrid = [0] * dimX
                for x in range(dimX):
                    self.qubitgrid[x] = [-1] * dimY

            if line[0] == "q":
                x = int(line[1])
                y = int(line[2])
                self.qubitgrid[x][y] = qubit_id
                qubit_id += 1

            if line[0] == "bustype":
                bustype = int(line[1])
                if bustype == 2:
                    self.generatefromAll2QBus()
                if bustype == 4:
                    self.generatefromAll2QBus()

            if line[0] == "b":
                x = int(line[1])
                y = int(line[2])
                self.crossbuslist.append([x, y])
        self.Patch4QBus()
        return
