import pytest
from qiskit import QuantumRegister, QuantumCircuit
from mqhad.architecture_generator.generator import Generator
from collections import OrderedDict


class TestGenerator:
    def test_setting_wrong_quantum_circuit(self):
        generator = Generator()
        with pytest.raises(ValueError):
            generator.quantum_circuit = None

    def test_get_mapping_two_qubit_gates(self):
        qr = QuantumRegister(5)
        qc = QuantumCircuit(qr)
        qc.h([0, 1, 2, 3])
        qc.x(4)
        qc.cx(0, 1)
        qc.h(4)
        qc.cx(0, 4)
        qc.h(0)
        qc.cx(1, 4)
        qc.cx(2, 4)
        qc.cx(3, 4)
        qc.cx(0, 4)

        generator = Generator()
        generator.quantum_circuit = qc
        interaction_map = generator._get_mapping_two_qubit_gates()
        assert interaction_map == OrderedDict(
            [((0, 1), 1), ((0, 4), 2), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )
