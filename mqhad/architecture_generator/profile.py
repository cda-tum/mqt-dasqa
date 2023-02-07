from collections import OrderedDict
from qiskit import QuantumCircuit
import numpy as np


class Profile:
    def _get_mapping_two_qubit_gates(self, qc: QuantumCircuit) -> list[list[int, int]]:
        """Traverse the circuit data, find the CX gates and store interaction count
        between control and target qubits

        Args:
            qc (QuantumCircuit): QuantumCircuit

        Returns:
            OrderedDict[tuple[int,int],int]: Map of (control_qubit, target_qubit) to number
            of interactions
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
        return L

    def _get_circuit_adjacency_matrix(
        self, num_qubits: int, two_qubit_map: list[list[int, int]]
    ) -> np.ndarray:
        """Two qubit map to adjacency matrix

        Returns:
            np.ndarray: adjacency matrix
        """
        adjacency_matrix = np.zeros((num_qubits, num_qubits), dtype=int)

        for control_qubit, target_qubit in two_qubit_map:
            adjacency_matrix[control_qubit, target_qubit] += 1
            adjacency_matrix[target_qubit, control_qubit] += 1

        return adjacency_matrix.tolist()

    def _get_circuit_ordered_degree(
        self, num_qubits: int, adjacency_matrix: np.ndarray
    ) -> list[tuple[int, int]]:
        degree_list = list(zip(range(num_qubits), np.sum(adjacency_matrix, axis=1)))
        ordered_degree = sorted(degree_list, key=lambda x: x[1], reverse=True)
        return ordered_degree

    def _get_interaction_count(
        self, two_qubit_map: list[list[int, int]]
    ) -> OrderedDict[tuple[int, int], int]:
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
        self, L: OrderedDict[tuple[int, int], int]
    ) -> OrderedDict[tuple[int, int], int]:
        return OrderedDict(sorted(L.items(), key=lambda x: x[1], reverse=True))
