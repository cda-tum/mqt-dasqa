import copy
import pickle
from .optimal_geometry_finder_base import OptimalGeometryFinderBase
from .metal import OptimalGeometryFinder as MetalOptimalGeometryFinder


class OptimalGeometryFinder(OptimalGeometryFinderBase):
    def __init__(self, design_backend: str = "metal", config: dict = {}):
        self._design_backend = design_backend
        self._config = config
        if self._design_backend == "metal":
            self._models = config["model"]
            self._models = self._unpack_models()
            self._optimal_geometry_finder = MetalOptimalGeometryFinder(self._models)

    def _unpack_models(self):
        models = copy.deepcopy(self._models)
        qubit_models = models["qubit"]
        for parameter, geometries in qubit_models.items():
            for geometry, model_path in geometries.items():
                with open(model_path, "rb") as file:
                    qubit_models[parameter][geometry] = pickle.load(file)
        return models

    def find_optimal_geometry(
        self, target_parameter: str, target_parameter_value: float
    ):
        return self._optimal_geometry_finder.find_optimal_geometry(
            target_parameter, target_parameter_value
        )
