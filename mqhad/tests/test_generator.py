import pytest
from qiskit import QuantumRegister, QuantumCircuit
from mqhad.architecture_generator.generator import Generator
from collections import OrderedDict


class TestGenerator:
    def test_setting_wrong_quantum_circuit(self):
        generator = Generator()
        with pytest.raises(ValueError):
            generator.quantum_circuit = None
