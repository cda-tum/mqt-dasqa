from abc import ABC, abstractmethod


class CapacitorLaunchpadConnectorBase(ABC):
    @abstractmethod
    def generate_capacitor_launchpad_connection(self):
        pass
