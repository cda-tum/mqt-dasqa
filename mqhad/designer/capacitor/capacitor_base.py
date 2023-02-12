from abc import ABC, abstractmethod


class CapacitorBase(ABC):
    @abstractmethod
    def generate_capacitor(self):
        pass
