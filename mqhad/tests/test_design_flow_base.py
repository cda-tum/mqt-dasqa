import pytest
from mqhad.design_flow_base import DesignFlowBase


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
        assert (
            "Qubit grid not generated. Please run generate_architecture() first."
            in str(excinfo.value)
        )

    def test_invalid_qubit_frequencies(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.qubit_frequencies
        assert (
            "Qubit frequencies not generated. Please run generate_architecture() first."
            in str(excinfo.value)
        )

    def test_invalid_canvas(self):
        with pytest.raises(ValueError) as excinfo:
            design_flow_mock = DesignFlowMock()
            design_flow_mock.canvas
        assert (
            "Physical design not generated. Please run map_to_physical_layout() first."
            in str(excinfo.value)
        )
