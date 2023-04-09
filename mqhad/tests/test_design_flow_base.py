import pytest
from mqhad.design_flow_base import DesignFlowBase


class DesignFlowMock(DesignFlowBase):
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
            DesignFlowMock()
        assert "Circuit path does not exist." in str(excinfo.value)

    def test_valid_circuit_path(self, tmp_path):
        # Create a file in the temporary directory
        temp_file = tmp_path / "test.qasm"
        temp_file.write_text("This is a temporary file.")
        path = str(temp_file)
        design_flow_mock = DesignFlowMock(circuit_path=path)
        assert design_flow_mock.circuit_path == path
