from abc import ABC, abstractmethod
from qiskit import QuantumCircuit


class GeneratorBase(ABC):
    @abstractmethod
    def generate(self):
        pass
