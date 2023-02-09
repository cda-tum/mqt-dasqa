from abc import ABC, abstractmethod


class YieldSimulatorBase(ABC):
    @abstractmethod
    def reset_seed(self, seed: int):
        pass

    @abstractmethod
    def simulate(self) -> tuple[float, float]:
        pass
