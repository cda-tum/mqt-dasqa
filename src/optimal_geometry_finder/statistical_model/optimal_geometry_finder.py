from typing import Any
import copy
import pickle
from ..optimal_geometry_finder_base import OptimalGeometryFinderBase


class OptimalGeometryFinder(OptimalGeometryFinderBase):
    def __init__(self, config: dict = {}):
        self._models_config = config["model"]
        self._models = self._unpack_models()

    def _unpack_models(self):
        models = copy.deepcopy(self._models_config)
        qubit_models = models["qubit"]
        for parameter, geometries in qubit_models.items():
            for geometry, model_path in geometries.items():
                with open(model_path, "rb") as file:
                    qubit_models[parameter][geometry] = pickle.load(file)
        return models

    def find_optimal_geometry(
        self, component: str, target_parameter: str, target_parameter_value: float
    ):
        result = {}
        if target_parameter not in self._models[component].keys():
            return result

        for geometry, model in self._models[component][target_parameter].items():
            prediction = model.predict([[target_parameter_value]])[0]
            result[geometry] = f"{prediction}um"
        return result
