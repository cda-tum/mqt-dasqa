from abc import ABC, abstractmethod
import numpy as np


class ProfileBase(ABC):
    @abstractmethod
    def get_profile(self) -> tuple[np.ndarray, np.ndarray]:
        pass
