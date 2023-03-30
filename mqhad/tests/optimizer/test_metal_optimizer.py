from unittest.mock import patch


class TestOptimizer:
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

            optimizer = Optimizer(models=models)
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
