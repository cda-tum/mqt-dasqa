from collections import OrderedDict
from qiskit import QuantumCircuit, QuantumRegister
from mqhad.architecture_generator.profile import Profile


class TestProfile:
    def test_get_mapping_two_qubit_gates(self):
        profile = Profile()
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

        mapping_two_qubit = profile._get_mapping_two_qubit_gates(qc)
        assert mapping_two_qubit == [[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]]

    def test_get_circuit_adjacency_matrix(self):
        profile = Profile()
        num_qubits = 5
        two_qubit_map = [[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]]
        adjacency_matrix = profile._get_circuit_adjacency_matrix(
            num_qubits, two_qubit_map
        )
        assert adjacency_matrix == [
            [0, 1, 0, 0, 2],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [2, 1, 1, 1, 0],
        ]

    def test_get_circuit_ordered_degree(self):
        profile = Profile()
        num_qubits = 5
        adjacency_matrix = [
            [0, 1, 0, 0, 2],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [2, 1, 1, 1, 0],
        ]
        ordered_degree = profile._get_circuit_ordered_degree(
            num_qubits, adjacency_matrix
        )
        assert ordered_degree == [(4, 5), (0, 3), (1, 2), (2, 1), (3, 1)]

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
