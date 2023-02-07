from collections import OrderedDict
from qiskit import QuantumCircuit, QuantumRegister
from mqhad.architecture_generator.profile import Profile


class TestProfile:
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

        profile = Profile()
        mapping_two_qubit = profile._get_mapping_two_qubit_gates(qc)
        assert mapping_two_qubit == [[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]]

    def test_get_interaction_count(self):
        profile = Profile()
        two_qubit_map = [[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]]
        interaction_count = profile._get_interaction_count(two_qubit_map)
        assert interaction_count == OrderedDict(
            [((0, 1), 1), ((0, 4), 2), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )

    def test_sort_interaction_dict(self):
        profile = Profile()
        L = OrderedDict(
            [((0, 1), 1), ((0, 4), 2), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )
        L_sorted = OrderedDict(
            [((0, 4), 2), ((0, 1), 1), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )
        assert profile._sort_interaction_dict(L) == L_sorted
