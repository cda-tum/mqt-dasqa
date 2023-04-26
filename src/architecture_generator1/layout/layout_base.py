from abc import ABC, abstractmethod
import numpy as np


class LayoutBase(ABC):
    @abstractmethod
    def get_layout(self) -> tuple[np.ndarray, np.ndarray]:
        pass
