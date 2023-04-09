from ..optimizer_base import OptimizerBase
import copy
import pickle
import numpy as np
from mqhad.mapper.canvas.canvas_base import CanvasBase
from mqhad.optimal_geometry_finder.optimal_geometry_finder import OptimalGeometryFinder


class Optimizer(OptimizerBase):
    def __init__(
        self,
        canvas: CanvasBase = None,
        qubit_frequencies: np.ndarray = [],
        config: dict = {},
        optimal_geometry_finder: OptimalGeometryFinder = None,
    ):
        """Optimizer class for metal designs

        Args:
            canvas (Canvas): Canvas
            qubit_frequencies (np.ndarray, optional): Array of qubit frequencies
            config (dict, optional): Config dict
        """
        self._canvas = canvas
        self._qubit_frequences = qubit_frequencies
        self._config = config
        self._optimal_geometry_finder = optimal_geometry_finder

    def optimize(self):
        merged_config = self._merge_config_with_qubit_frequencies(
            self._qubit_frequences, self._config
        )
        processed_config = self._process_config(merged_config)
        self._targets = processed_config["target"]
        self._models = processed_config["model"]
        self._models = self._unpack_models()
        self._optimize_qubits()
        self._optimize_resonators()

    def _merge_config_with_qubit_frequencies(
        self, qubit_frequencies: np.ndarray, config: dict
    ) -> dict:
        """Merge config dict with qubit frequencies

        Args:
            qubit_frequencies (np.ndarray): Array of qubit frequencies
            config (dict): Config dict

        Returns:
            dict: Config dict with qubit frequencies
        """
        tmp = copy.deepcopy(config)
        qubit_specific = tmp["target"]["qubit"]["specific"]
        if qubit_specific is None:
            qubit_specific = {}
            tmp["target"]["qubit"]["specific"] = qubit_specific

        for i, qubit_frequency in enumerate(qubit_frequencies):
            qubit_name = f"Q_{i}"

            # If qubit configuration already exist in config.yml
            # don't overwrite it
            if qubit_name in qubit_specific:
                continue

            qubit_specific[qubit_name] = {}
            qubit_specific[qubit_name]["fQ"] = qubit_frequency
        return tmp

    def _process_config(self, config: dict) -> dict:
        """Merge general component parameters with specific component parameters

        Args:
            config (dict): config dict

        Returns:
            dict: processed config
        """
        tmp = copy.deepcopy(config)
        qubit_specific = tmp["target"]["qubit"]["specific"]
        qubit_general = tmp["target"]["qubit"]["general"]

        if qubit_general == None:
            return tmp

        for qubit, _ in qubit_specific.items():
            qubit_specific[qubit].update(qubit_general)
        return tmp

    def _unpack_models(self):
        models = copy.deepcopy(self._models)
        qubit_models = models["qubit"]
        for parameter, geometries in qubit_models.items():
            for geometry, model_path in geometries.items():
                with open(model_path, "rb") as file:
                    qubit_models[parameter][geometry] = pickle.load(file)
        return models

    def _optimize_qubits(self):
        for qubit, parameters in self._targets["qubit"]["specific"].items():
            for parameter, target_value in parameters.items():
                geometries = self._optimal_geometry_finder.find_optimal_geometry(
                    component="qubit",
                    target_parameter=parameter,
                    target_parameter_value=target_value,
                )
                for geometry_name, geometry_value in geometries.items():
                    self._canvas.update_components(qubit, geometry_name, geometry_value)
                    # self._canvas.components[qubit].options[
                    #     geometry_name
                    # ] = geometry_value

    def _optimize_resonators(self):
        pass
