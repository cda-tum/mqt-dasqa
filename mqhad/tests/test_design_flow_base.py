import pytest
import numpy as np
from mqhad.design_flow_base import DesignFlowBase
from mqhad.mapper.canvas.metal import Canvas as MetalCanvas


class DesignFlowMock(DesignFlowBase):
    def __init__(self):
        pass

    def generate_architecture(self):
        pass

    def map_to_physical_layout(self):
        pass

    def optimize_design(self):
        pass

    def display_gui(self):
        pass

    # Hooks
    def read_circuit(self):
        pass


class TestDesignFlowBase:
    def test_invalid_circuit_path(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.circuit_path = "invalid_path"
        assert "Circuit path does not exist." in str(excinfo.value)

    def test_valid_circuit_path(self, tmp_path):
        # Create a file in the temporary directory
        temp_file = tmp_path / "test.qasm"
        temp_file.write_text("This is a temporary file.")
        path = str(temp_file)
        design_flow_mock = DesignFlowMock()
        design_flow_mock.circuit_path = path
        assert design_flow_mock.circuit_path == path

    def test_invalid_qubit_grid(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.qubit_grid
        assert "Qubit grid not generated." in str(excinfo.value)

    def test_invalid_qubit_frequencies(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.qubit_frequencies
        assert "Qubit frequencies not generated." in str(excinfo.value)

    def test_invalid_canvas(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.canvas
        assert "Physical layout not generated." in str(excinfo.value)

    def test_qubit_grid_setter_list(self):
        design_flow_mock = DesignFlowMock()
        design_flow_mock.qubit_grid = [[0, 0], [0, 1]]
        assert isinstance(design_flow_mock.qubit_grid, np.ndarray)
        np.testing.assert_array_equal(
            design_flow_mock.qubit_grid, np.array([[0, 0], [0, 1]])
        )

    def test_qubit_grid_setter_ndarray(self):
        design_flow_mock = DesignFlowMock()
        design_flow_mock.qubit_grid = np.array([[0, 0], [0, 1]])
        assert isinstance(design_flow_mock.qubit_grid, np.ndarray)
        np.testing.assert_array_equal(
            design_flow_mock.qubit_grid, np.array([[0, 0], [0, 1]])
        )

    def test_qubit_grid_setter_invalid(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.qubit_grid = 1
        assert "Qubit grid must be a 2D array." in str(excinfo.value)

    def test_qubit_frequencies_setter_list(self):
        design_flow_mock = DesignFlowMock()
        design_flow_mock.qubit_frequencies = [1, 2]
        assert isinstance(design_flow_mock.qubit_frequencies, np.ndarray)
        np.testing.assert_array_equal(
            design_flow_mock.qubit_frequencies, np.array([1, 2])
        )

    def test_qubit_frequencies_setter_ndarray(self):
        design_flow_mock = DesignFlowMock()
        design_flow_mock.qubit_frequencies = np.array([1, 2])
        assert isinstance(design_flow_mock.qubit_frequencies, np.ndarray)
        np.testing.assert_array_equal(
            design_flow_mock.qubit_frequencies, np.array([1, 2])
        )

    def test_qubit_frequencies_setter_invalid(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.qubit_frequencies = 1
        assert "Qubit frequencies must be a 1D array." in str(excinfo.value)

    def test_canvas_setter(self):
        design_flow_mock = DesignFlowMock()
        design_flow_mock.canvas = MetalCanvas()
        assert isinstance(design_flow_mock.canvas, MetalCanvas)

    def test_canvas_setter_invalid(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.canvas = 1
        assert "Canvas must be an instance of Canvas." in str(excinfo.value)
