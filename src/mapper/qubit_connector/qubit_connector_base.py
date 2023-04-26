from abc import ABC, abstractmethod


class QubitConnectorBase(ABC):
    @abstractmethod
    def generate_qubit_connection(self):
        pass
