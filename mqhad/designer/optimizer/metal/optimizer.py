from ..optimizer_base import OptimizerBase
import copy
import pickle
import numpy as np
from qiskit_metal.designs import DesignPlanar


class Optimizer(OptimizerBase):
    def __init__(self, design=None, config: dict = {}):  #: DesignPlanar = None,
        """Optimizer class for metal designs

        Args:
            design (DesignPlanar): Metal design
            targets (dict): Target values for each target
            {
                "target": {
                    "qubit": {
                        "specific": {"Q_0": {"fQ": 5.3, "EC/EQ": 50}},
                        "general": {"EC/EQ": 50},
                    },
                    "resonator": {
                        "specific": {"CU_0": {"fQ": 5.3}},
                        "general": None,
                    },
                },
            }
            models (dict): Model paths for each target
            {
                "model": {
                    "qubit": {
                        "fQ": {
                            "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                            "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                        }
                    },
                    "resonator": None,
                },
            }
        """
        self._design = design
        self._config = config

    def optimize(self):
        merged_dict = self._merge_config_dict_with_qubit_frequencies(self._config)
        processed_config = self._process_config_dict(merged_dict)
        self._targets = processed_config["target"]
        self._models = processed_config["model"]
        self._models = self._unpack_models()
        self._optimize_qubits()
        self._optimize_resonators()

    def _merge_config_dict_with_qubit_frequencies(
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
        for i, qubit_frequency in enumerate(qubit_frequencies):
            qubit_name = f"Q_{i}"

            # If qubit configuration already exist in config.yml
            # don't overwrite it
            if qubit_name in qubit_specific:
                continue

            qubit_specific[qubit_name] = {}
            qubit_specific[qubit_name]["fQ"] = qubit_frequency
        return tmp

    def _process_config_dict(self, config: dict) -> dict:
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
                for _, model in self._models["qubit"][parameter].items():
                    geometry_value = model.predict([[target_value]])[0]
                    self._design.components[qubit].options[
                        parameter
                    ] = f"{geometry_value}um"

    def _optimize_resonators(self):
        pass
