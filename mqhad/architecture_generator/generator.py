from collections import OrderedDict
from mqhad.architecture_generator.generator_base import GeneratorBase


class Generator(GeneratorBase):
    def __init__(
        self,
    ) -> None:
        pass

    def generate(self):
        pass

    def _get_mapping_two_qubit_gates(self) -> OrderedDict[tuple[int, int], int]:
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
        L = OrderedDict()
        for operation in self.qc.data:
            gate = operation[0]
            if gate.name == "cx":
                control_qubit = self.qc.find_bit(operation.qubits[0]).index
                target_qubit = self.qc.find_bit(operation.qubits[1]).index
                key = (control_qubit, target_qubit)
                interaction = L.get(key, 0)
                if interaction == 0:
                    L[key] = 1
                else:
                    L[key] += 1
        return L
