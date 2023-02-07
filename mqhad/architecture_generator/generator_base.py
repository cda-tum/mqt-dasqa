from abc import ABC, abstractmethod
from qiskit import QuantumCircuit


class GeneratorBase(ABC):
    @abstractmethod
    def generate(self):
        pass

    @property
    def quantum_circuit(self):
        return self.qc

    @quantum_circuit.setter
    def quantum_circuit(self, qc: QuantumCircuit):
        if not isinstance(qc, QuantumCircuit):
            raise ValueError("qc needs to be a instance of QuantumCircuit")
        else:
            self.qc = qc
