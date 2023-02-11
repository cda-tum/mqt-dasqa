from unittest import mock
import argparse


class TestMain:
    # Check for no exceptions
    def test_main(self):
        with mock.patch(
            "mqhad.architecture_generator.generator.Generator"
        ) as mock_class:
            from mqhad.__main__ import flow

            instance = mock_class.return_value
            qubit_grid = [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]]
            qubit_frequencies = [
                5.339999999999993,
                5.339999999999993,
                5.339999999999993,
                5.339999999999993,
                5.17,
            ]
            instance.generate = mock.MagicMock(
                return_value=(qubit_grid, qubit_frequencies)
            )
            args = argparse.Namespace(
                file_path="./mqhad/tests/test_circuit/circuit1.qasm"
            )
            flow(args)
