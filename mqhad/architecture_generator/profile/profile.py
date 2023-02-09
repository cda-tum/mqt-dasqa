from collections import OrderedDict
from qiskit import QuantumCircuit
import numpy as np
from .profile_base import ProfileBase


class Profile(ProfileBase):
    def __init__(self, qc: QuantumCircuit):
        self.qc = qc
        self.num_qubits = qc.num_qubits

    def get_profile(self) -> tuple[np.ndarray, np.ndarray]:
        self.two_qubit_map = self._get_mapping_two_qubit_gates(self.qc)
        self.adjacency_matrix = self._get_circuit_adjacency_matrix(
            self.num_qubits, self.two_qubit_map
        )
        self.ordered_degree = self._get_circuit_ordered_degree(
            self.num_qubits, self.adjacency_matrix
        )
        return self.ordered_degree, self.adjacency_matrix

    def _get_mapping_two_qubit_gates(self, qc: QuantumCircuit) -> np.ndarray[int]:
        """Get mapping of two qubit gates

        Args:
            qc (QuantumCircuit): Quantum circuit

        Returns:
            np.ndarray: Mapping of two qubit gates
        """
        # Traverse the circuit data, find the CX gates and store interaction count
        # between control and target qubits
        L = []
        for operation in qc.data:
            gate = operation[0]
            if gate.name == "cx":
                control_qubit = qc.find_bit(operation.qubits[0]).index
                target_qubit = qc.find_bit(operation.qubits[1]).index
                L.append([control_qubit, target_qubit])
        return np.array(L)

    def _get_circuit_adjacency_matrix(
        self, num_qubits: int, two_qubit_map: np.ndarray[int]
    ) -> np.ndarray[int]:
        """Get adjacency matrix of the circuit

        Args:
            num_qubits (int): Number of qubits
            two_qubit_map (np.ndarray[int]): Mapping of two qubit gates

        Returns:
            np.ndarray[int]: Adjacency matrix of the circuit
        """
        adjacency_matrix = np.zeros((num_qubits, num_qubits), dtype=int)

        for control_qubit, target_qubit in two_qubit_map:
            adjacency_matrix[control_qubit][target_qubit] += 1
            adjacency_matrix[target_qubit][control_qubit] += 1

        return adjacency_matrix

    def _get_circuit_ordered_degree(
        self, num_qubits: int, adjacency_matrix: np.ndarray[int]
    ) -> np.ndarray[int]:
        """Get ordered degree of the circuit

        Args:
            num_qubits (int): Number of qubits
            adjacency_matrix (np.ndarray[int]): Adjacency matrix of the circuit

        Returns:
            np.ndarray[int]: Ordered degree of the circuit
        """
        degrees = np.sum(adjacency_matrix, axis=1)
        degree_list = list(zip(range(num_qubits), degrees))
        ordered_degree = sorted(degree_list, key=lambda x: x[1], reverse=True)
        return ordered_degree

    def _get_interaction_count(
        self, two_qubit_map: np.ndarray[int]
    ) -> OrderedDict[tuple[int, int], int]:
        """Get interaction count of the circuit

        Args:
            two_qubit_map (np.ndarray[int]): Mapping of two qubit gates

        Returns:
            OrderedDict[tuple[int, int], int]: Interaction count of the circuit
        """
        interaction_count_map = OrderedDict()
        for qubits in two_qubit_map:
            qubits_ = tuple(qubits)
            interaction = interaction_count_map.get(qubits_, 0)
            if interaction == 0:
                interaction_count_map[qubits_] = 1
            else:
                interaction_count_map[qubits_] += 1
        return interaction_count_map

    def _sort_interaction_dict(
        self, interaction_count: OrderedDict[tuple[int, int], int]
    ) -> OrderedDict[tuple[int, int], int]:
        """Sort interaction count of the circuit

        Args:
            interaction_count (OrderedDict[tuple[int, int], int]): Interaction count of the circuit

        Returns:
            OrderedDict[tuple[int, int], int]: Sorted interaction count of the circuit
        """
        return OrderedDict(
            sorted(interaction_count.items(), key=lambda x: x[1], reverse=True)
        )
