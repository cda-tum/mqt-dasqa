from abc import ABC, abstractmethod


class OptimizerBase(ABC):
    @abstractmethod
    def optimize(self):
        pass
