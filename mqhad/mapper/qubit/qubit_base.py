from abc import ABC, abstractmethod


class QubitBase(ABC):
    @abstractmethod
    def generate_qubit_layout(self):
        pass
