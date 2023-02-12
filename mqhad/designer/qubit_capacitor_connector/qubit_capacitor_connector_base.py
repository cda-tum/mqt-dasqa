from abc import ABC, abstractmethod


class QubitCapacitorConnectorBase(ABC):
    @abstractmethod
    def generate_qubit_capacitor_connection(self):
        pass
