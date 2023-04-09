from abc import ABC, abstractmethod

class OptimalGeometryFinderBase(ABC):

    @abstractmethod
    def find_optimal_geometry(self, target_parameter: str, target_parameter_value: float):
        pass