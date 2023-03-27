from ..optimizer_base import OptimizerBase

class Optimizer(OptimizerBase):
    def __init__(self, design, qubit_grid):
        self._design = design

    def optimize(self):
        pass