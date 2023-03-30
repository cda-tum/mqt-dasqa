from ..optimizer_base import OptimizerBase
import copy
import pickle

from qiskit_metal.designs import DesignPlanar


class Optimizer(OptimizerBase):
    def __init__(
        self,
        design=None,  #: DesignPlanar = None,
        targets: dict = {},
        models: dict = {},
    ):
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
        self._models = models
        self._targets = targets

    def optimize(self):
        self._models = self._unpack_models()
        self._optimize_qubits()
        self._optimize_resonators()

    def _unpack_models(self):
        models = copy.deepcopy(self._models)
        qubit_models = models["qubit"]
        for parameter, geometries in qubit_models.items():
            for geometry, model_path in geometries.items():
                qubit_models[parameter][geometry] = pickle.load(model_path)
        return models

    def _optimize_qubits(self):
        for qubit, parameters in self._targets["qubit"].items():
            for parameter, target_value in parameters.items():
                for _, model in self._models["qubit"][parameter].items():
                    geometry_value = model.predict(target_value)
                    self._design.components[qubit].options[parameter] = geometry_value

    def _optimize_resonators(self):
        pass
