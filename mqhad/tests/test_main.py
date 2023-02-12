from unittest import mock
import argparse


class TestMain:
    # Check for no exceptions
    @mock.patch("mqhad.architecture_generator.generator.Generator")
    @mock.patch("mqhad.designer.design.Design")
    def test_main(self, mock_class2, mock_class1):
        from mqhad.__main__ import flow

        instance = mock_class1.return_value
        qubit_grid = [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]]
        qubit_frequencies = [
            5.339999999999993,
            5.339999999999993,
            5.339999999999993,
            5.339999999999993,
            5.17,
        ]
        instance.generate = mock.MagicMock(return_value=(qubit_grid, qubit_frequencies))
        output1 = {
            "qubit_grid": qubit_grid,
            "qubit_frequencies": qubit_frequencies,
        }
        instance2 = mock_class2.return_value
        instance2.design = mock.MagicMock()
        args = argparse.Namespace(file_path="./mqhad/tests/test_circuit/circuit1.qasm")
        flow(args)

    def test_main_invalid_file_path(self, capfd):
        from mqhad.__main__ import flow

        args = argparse.Namespace(file_path="./invalid_file.qasm")
        flow(args)
        # Capture the stdout and stderr output
        out, err = capfd.readouterr()
        assert out == "File does not exist. Exiting...\n"
