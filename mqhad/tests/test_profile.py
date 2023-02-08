from collections import OrderedDict
from qiskit import QuantumCircuit, QuantumRegister
from mqhad.architecture_generator.profile import Profile
import numpy as np


class TestProfile:
    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
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
        cls.qc = qc

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to
        setup_class.
        """
        pass

    def test_get_profile(self):
        profile = Profile(self.qc)
        ordered_degree, adjacency_matrix = profile.get_profile()
        np.testing.assert_array_equal(
            ordered_degree, [[4, 5], [0, 3], [1, 2], [2, 1], [3, 1]]
        )
        np.testing.assert_array_equal(
            adjacency_matrix,
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ],
        )

    def test_get_mapping_two_qubit_gates(self):
        profile = Profile(self.qc)

        mapping_two_qubit = profile._get_mapping_two_qubit_gates(self.qc)
        np.testing.assert_array_equal(
            mapping_two_qubit, [[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]]
        )

    def test_get_circuit_adjacency_matrix(self):
        profile = Profile(self.qc)
        num_qubits = 5
        two_qubit_map = np.array([[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]])
        adjacency_matrix = profile._get_circuit_adjacency_matrix(
            num_qubits, two_qubit_map
        )
        np.testing.assert_array_equal(
            adjacency_matrix,
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ],
        )

    def test_get_circuit_ordered_degree(self):
        profile = Profile(self.qc)
        num_qubits = 5
        adjacency_matrix = np.array(
            [
                [0, 1, 0, 0, 2],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [2, 1, 1, 1, 0],
            ]
        )
        ordered_degree = profile._get_circuit_ordered_degree(
            num_qubits, adjacency_matrix
        )
        np.testing.assert_array_equal(
            ordered_degree, [[4, 5], [0, 3], [1, 2], [2, 1], [3, 1]]
        )

    def test_get_interaction_count(self):
        profile = Profile(self.qc)
        two_qubit_map = [[0, 1], [0, 4], [1, 4], [2, 4], [3, 4], [0, 4]]
        interaction_count = profile._get_interaction_count(two_qubit_map)
        assert interaction_count == OrderedDict(
            [((0, 1), 1), ((0, 4), 2), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )

    def test_sort_interaction_dict(self):
        profile = Profile(self.qc)
        L = OrderedDict(
            [((0, 1), 1), ((0, 4), 2), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )
        L_sorted = OrderedDict(
            [((0, 4), 2), ((0, 1), 1), ((1, 4), 1), ((2, 4), 1), ((3, 4), 1)]
        )
        assert profile._sort_interaction_dict(L) == L_sorted
