from abc import ABC, abstractmethod


class QubitConnectionBase(ABC):
    @abstractmethod
    def generate_qubit_connection(self):
        pass
