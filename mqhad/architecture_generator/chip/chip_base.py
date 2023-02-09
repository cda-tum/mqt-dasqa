from abc import ABC, abstractmethod
import numpy as np


class ChipBase(ABC):
    @property
    @abstractmethod
    def adjacency_matrix(self) -> np.ndarray:
        pass

    @property
    @abstractmethod
    def coupling_list(self) -> np.ndarray:
        pass

    @coupling_list.setter
    @abstractmethod
    def coupling_list(self, coupling_list: list[list[int]]):
        pass

    @property
    @abstractmethod
    def grid_edge_list(self) -> np.ndarray:
        pass

    @grid_edge_list.setter
    @abstractmethod
    def grid_edge_list(self, grid_edge_list: list[list[int]]):
        pass

    @property
    @abstractmethod
    def via_edge_list(self) -> np.ndarray:
        pass

    @via_edge_list.setter
    @abstractmethod
    def via_edge_list(self, via_edge_list: list[list[int]]):
        pass

    @property
    @abstractmethod
    def edge_list(self) -> np.ndarray:
        pass

    @edge_list.setter
    @abstractmethod
    def edge_list(self, edge_list: list[list[int]]):
        pass

    @abstractmethod
    def generate_buses(self):
        pass
