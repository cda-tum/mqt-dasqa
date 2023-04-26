from unittest.mock import patch, MagicMock
import os
from sklearn.pipeline import Pipeline


class TestOptimizer:
    def test_merge_config_with_qubit_frequencies(self):
        from src.optimizer.metal import Optimizer

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
                "qubit": {"specific": {"Q_0": {"fQ": 5.3}}, "general": {"EC/EJ": 50}},
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        qubit_frequencies = [5.2, 5.8]
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
                    "specific": {"Q_0": {"fQ": 5.3}, "Q_1": {"fQ": 5.8}},
                    "general": {"EC/EJ": 50},
                },
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        output = optimizer._merge_config_with_qubit_frequencies(
            qubit_frequencies, config
        )
        assert output == result

    def test_merge_config_with_qubit_frequencies2(self):
        # Test when qubit specific config is None
        from src.optimizer.metal import Optimizer

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
                "qubit": {"specific": None, "general": {"EC/EJ": 50}},
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        qubit_frequencies = [5.2, 5.8]
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
                    "specific": {"Q_0": {"fQ": 5.2}, "Q_1": {"fQ": 5.8}},
                    "general": {"EC/EJ": 50},
                },
                "resonator": {"specific": {"CU_0": {"fQ": 5.3}}, "general": None},
            },
        }
        output = optimizer._merge_config_with_qubit_frequencies(
            qubit_frequencies, config
        )
        assert output == result

    def test_process_config(self):
        from src.optimizer.metal import Optimizer

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
                "qubit": {"specific": {"Q_0": {"fQ": 5.3}}, "general": {"EC/EJ": 50}},
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
                    "specific": {"Q_0": {"fQ": 5.3, "EC/EJ": 50}},
                    "general": {"EC/EJ": 50},
                },
                "resonator": {
                    "specific": {"CU_0": {"fQ": 5.3}},
                    "general": None,
                },
            },
        }
        output = optimizer._process_config(config)
        assert output == result

    def test_process_config2(self):
        # Test NoneType for config["target"]["qubit"]["general"]
        from src.optimizer.metal import Optimizer

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
        output = optimizer._process_config(config)
        assert output == result

    def test_unpack_models(self):
        # DesignPlanar needs to be patched first as builtins.open messes up
        # Matplotlib which is supposedly used by DesignPlanar
        with patch("qiskit_metal.designs.DesignPlanar"), patch("builtins.open"), patch(
            "pickle.load"
        ) as mock_load:
            mock_load.return_value = "model_unpacked"
            from src.optimizer.metal import Optimizer

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
        from src.optimizer.metal import Optimizer

        models = {
            "qubit": {
                "fQ": {
                    "pad_gap": os.getcwd()
                    + "/src/tests/test_model/polynomial_ridge_regression_fQ_pad_gap_in_um.pkl",
                }
            },
            "resonator": None,
        }

        optimizer = Optimizer()
        optimizer._models = models
        unpacked_models = optimizer._unpack_models()
        assert type(unpacked_models["qubit"]["fQ"]["pad_gap"]) == Pipeline

    def test_optimize_qubits(self):
        from src.optimizer.metal import Optimizer

        optimizer = Optimizer()

        optimizer._targets = {
            "qubit": {
                "specific": {
                    "Q_0": {
                        "fQ": 5.3,
                        "EC/EJ": 50,  # Test case for not in list of supported models
                    }
                },
                "general": None,
            },
            "resonator": {
                "specific": None,
                "general": None,
            },
        }

        optimizer._optimal_geometry_finder = MagicMock()

        def find_optimal_geometry_side_effect(
            component: str, target_parameter: str, *args, **kwargs
        ):
            if target_parameter == "fQ":
                return {
                    "pad_gap": "10.0um",
                    "pad_height": "10.0um",
                }
            return {}

        optimizer._optimal_geometry_finder.find_optimal_geometry.side_effect = (
            find_optimal_geometry_side_effect
        )

        mock_canvas = MagicMock(name="mock_canvas")
        optimizer._canvas = mock_canvas

        optimizer._optimize_qubits()

        assert mock_canvas.update_component.call_count == 2
