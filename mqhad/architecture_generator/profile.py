from collections import OrderedDict
from qiskit import QuantumCircuit


class Profile:
    def __init__(self, qc: QuantumCircuit):
        self.qc = qc
        self.num_qubits = qc.num_qubits
        self.two_qubit_map = self._get_mapping_two_qubit_gates(qc)
        self.adjacency_matrix = self._get_circuit_adjacency_matrix(
            self.num_qubits, self.two_qubit_map
        )
        self.ordered_degree = self._get_circuit_ordered_degree(
            self.num_qubits, self.adjacency_matrix
        )

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
    ) -> list[list[int]]:
        """Two qubit map to adjacency matrix

        Returns:
            list[list[int]]: adjacency matrix
        """
        adjacency_matrix = [0] * num_qubits
        for qubit_id in range(num_qubits):
            adjacency_matrix[qubit_id] = [0] * num_qubits

        for control_qubit, target_qubit in two_qubit_map:
            adjacency_matrix[control_qubit][target_qubit] += 1
            adjacency_matrix[target_qubit][control_qubit] += 1

        return adjacency_matrix

    def _get_circuit_ordered_degree(
        self, num_qubits: int, adjacency_matrix: list[list[int]]
    ) -> list[tuple[int, int]]:
        degrees = [0] * num_qubits
        for qubit in range(num_qubits):
            for neighbor in range(num_qubits):
                degrees[qubit] += adjacency_matrix[qubit][neighbor]

        degree_list = list(zip(range(num_qubits), degrees))
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
