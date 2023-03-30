import pytest
import os
import yaml
from mqhad.utils import Utils


class TestUtils:
    def test_check_type_failure(self):
        with pytest.raises(TypeError):
            Utils.check_type("1", int)

    def test_check_type_failure_with_list(self):
        with pytest.raises(TypeError):
            Utils.check_type("1", [int, list])

    def test_check_type_failure_without_raise_error(self):
        result = Utils.check_type("1", int, raise_error=False)
        assert result == False

    def test_check_type_success(self):
        result = Utils.check_type(1, int)
        assert result == True

    # Test for no exception
    def test_load_yaml(self):
        CONFIG_FILE_PATH = os.getcwd() + "/mqhad/tests/test_config/config.yml"
        Utils.load_yaml(CONFIG_FILE_PATH)

    def test_process_config_dict(self):
        CONFIG_FILE_PATH = os.getcwd() + "/mqhad/tests/test_config/config.yml"
        config = Utils.load_yaml(CONFIG_FILE_PATH)
        output = Utils.process_config_dict(config)
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
                }
            },
        }
        assert output == result
