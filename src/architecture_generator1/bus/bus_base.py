from abc import ABC, abstractmethod
import numpy as np


class BusBase(ABC):
    @abstractmethod
    def bus_select(self) -> tuple[np.ndarray, np.ndarray]:
        pass
