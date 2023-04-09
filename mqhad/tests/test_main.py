from unittest.mock import patch, MagicMock
import argparse
from typing import Any
import numpy as np


class TestMain:
    # Check for no exceptions
    @patch("mqhad.concrete_design_flow1.ConcreteDesignFlow1")
    def test_main(self, mock_class1):
        from mqhad.__main__ import flow

        args = argparse.Namespace(
            file_path="./mqhad/tests/test_circuit/circuit1.qasm",
            config_file_path="./mqhad/tests/test_config/config.yml",
        )
        flow(args)

    # Check for no exceptions
    @patch("mqhad.architecture_generator1.generator.Generator")
    def test_main2(self, mock_class1):
        """Test main function without mock for design and optimizer.

        Args:
            mock_class1 (Generator): mock class for Generator
        """
        from mqhad.__main__ import flow

        instance = mock_class1.return_value
        qubit_grid = np.array([[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])
        qubit_frequencies = np.array(
            [
                5.339999999999993,
                5.339999999999993,
                5.339999999999993,
                5.339999999999993,
                5.17,
            ]
        )
        instance.generate = MagicMock(return_value=(qubit_grid, qubit_frequencies))

        args = argparse.Namespace(
            file_path="./mqhad/tests/test_circuit/circuit1.qasm",
            config_file_path="./mqhad/tests/test_config/config.yml",
        )
        flow(args)

    def test_main_valid_circuit_file_path(self, capfd):
        from mqhad.__main__ import check_file_path

        args = argparse.Namespace(file_path="./mqhad/tests/test_circuit/circuit1.qasm")
        circuit_absolute_path, exit_code = check_file_path(args)
        assert exit_code == 0

    def test_main_invalid_circuit_file_path(self, capfd):
        from mqhad.__main__ import check_file_path

        args = argparse.Namespace(file_path="./invalid_file.qasm")
        circuit_absolute_path, exit_code = check_file_path(args)
        assert circuit_absolute_path is None
        assert exit_code == 1
        # Capture the stdout and stderr output
        out, err = capfd.readouterr()
        assert out == "Circuit file does not exist. Exiting...\n"

    def test_main_valid_config_file_path(self, capfd):
        from mqhad.__main__ import check_file_path

        args = argparse.Namespace(file_path="./mqhad/tests/test_config/config.yml")
        config_absolute_path, exit_code = check_file_path(args)
        assert exit_code == 0

    def test_main_invalid_config_file_path(self, capfd):
        from mqhad.__main__ import check_config_file_path

        args = argparse.Namespace(config_file_path="./invalid_file.yml")
        config_absolute_path, exit_code = check_config_file_path(args)
        assert config_absolute_path is None
        assert exit_code == 1
        # Capture the stdout and stderr output
        out, err = capfd.readouterr()
        assert out == "Config file does not exist. Exiting...\n"

    # Test for no exception
    def test_load_yaml(self):
        from mqhad.__main__ import load_yaml

        CONFIG_FILE_PATH = "./mqhad/tests/test_config/config.yml"
        load_yaml(CONFIG_FILE_PATH)
