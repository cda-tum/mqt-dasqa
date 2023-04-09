from typing import Any
from ..optimal_geometry_finder_base import OptimalGeometryFinderBase


class OptimalGeometryFinder(OptimalGeometryFinderBase):
    def __init__(self, models: Any = None):
        self._models = models

    def find_optimal_geometry(
        self, component: str, target_parameter: str, target_parameter_value: float
    ):
        result = {}
        for geometry, model in self._models[component][target_parameter].items():
            prediction = model.predict([[target_parameter_value]])[0]
            result[geometry] = f"{prediction}um"
        return result
