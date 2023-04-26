from .optimal_geometry_finder_base import OptimalGeometryFinderBase
from .statistical_model import OptimalGeometryFinder as MetalOptimalGeometryFinder


class OptimalGeometryFinder(OptimalGeometryFinderBase):
    def __init__(self, design_backend: str = "metal", config: dict = {}):
        self._design_backend = design_backend
        self._config = config
        if self._design_backend == "metal":
            self._optimal_geometry_finder = MetalOptimalGeometryFinder(self._config)

    def find_optimal_geometry(
        self, component: str, target_parameter: str, target_parameter_value: float
    ):
        return self._optimal_geometry_finder.find_optimal_geometry(
            component, target_parameter, target_parameter_value
        )
