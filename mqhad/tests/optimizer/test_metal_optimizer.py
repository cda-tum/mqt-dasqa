from unittest.mock import patch, MagicMock
import os
from sklearn.pipeline import Pipeline


class TestOptimizer:
    def test_process_config_dict(self):
        from mqhad.designer.optimizer.metal import Optimizer

        optimizer = Optimizer()
        config = {
            "model": {
                "qubit": {
                    "fQ": {
                        "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                        "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                    }
                },
                "resonator": None,
            },
            "target": {
                "qubit": {"specific": {"Q_0": {"fQ": 5.3}}, "general": {"EC/EQ": 50}},
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        result = {
            "model": {
                "qubit": {
                    "fQ": {
                        "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                        "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                    }
                },
                "resonator": None,
            },
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
        output = optimizer._process_config_dict(config)
        assert output == result

    def test_process_config_dict2(self):
        # Test NoneType for config["target"]["qubit"]["general"]
        from mqhad.designer.optimizer.metal import Optimizer

        optimizer = Optimizer()
        config = {
            "model": {
                "qubit": {
                    "fQ": {
                        "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                        "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                    }
                },
                "resonator": None,
            },
            "target": {
                "qubit": {"specific": {"Q_0": {"fQ": 5.3}}, "general": None},
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        result = {
            "model": {
                "qubit": {
                    "fQ": {
                        "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                        "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                    }
                },
                "resonator": None,
            },
            "target": {
                "qubit": {
                    "specific": {"Q_0": {"fQ": 5.3}},
                    "general": None,
                },
                "resonator": {
                    "specific": {"CU_0": {"fQ": 5.3}},
                    "general": None,
                },
            },
        }
        output = optimizer._process_config_dict(config)
        assert output == result

    def test_unpack_models(self):
        # DesignPlanar needs to be patched first as builtins.open messes up
        # Matplotlib which is supposedly used by DesignPlanar
        with patch("qiskit_metal.designs.DesignPlanar"), patch("builtins.open"), patch(
            "pickle.load"
        ) as mock_load:
            mock_load.return_value = "model_unpacked"
            from mqhad.designer.optimizer.metal import Optimizer

            models = {
                "qubit": {
                    "fQ": {
                        "pad_gap": "models/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                        "pad_height": "models/polynomial_ridge_regression_fQ_pad_height_in_um.pkl",
                    }
                },
                "resonator": None,
            }

            optimizer = Optimizer()
            optimizer._models = models
            unpacked_models = optimizer._unpack_models()
            assert unpacked_models == {
                "qubit": {
                    "fQ": {
                        "pad_gap": "model_unpacked",
                        "pad_height": "model_unpacked",
                    }
                },
                "resonator": None,
            }

    def test_unpack_models2(self):
        # Real model file is used
        from mqhad.designer.optimizer.metal import Optimizer

        models = {
            "qubit": {
                "fQ": {
                    "pad_gap": os.getcwd()
                    + "/mqhad/tests/test_model/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                }
            },
            "resonator": None,
        }

        optimizer = Optimizer()
        optimizer._models = models
        unpacked_models = optimizer._unpack_models()
        assert type(unpacked_models["qubit"]["fQ"]["pad_gap"]) == Pipeline

    def test_optimize_qubits(self):
        from mqhad.designer.optimizer.metal import Optimizer

        optimizer = Optimizer()

        optimizer._targets = {
            "qubit": {
                "specific": {"Q_0": {"fQ": 5.3}},
                "general": None,
            },
            "resonator": {
                "specific": None,
                "general": None,
            },
        }
        mock_model = MagicMock()
        mock_model.predict.return_value = 10.0

        optimizer._models = {
            "qubit": {
                "fQ": {
                    "pad_gap": mock_model,
                    "pad_height": mock_model,
                }
            },
            "resonator": None,
        }

        mock_design = MagicMock(name="mock_design")
        optimizer._design = mock_design

        optimizer._optimize_qubits()

        assert mock_design.components.__getitem__().options.__setitem__.call_count == 2
