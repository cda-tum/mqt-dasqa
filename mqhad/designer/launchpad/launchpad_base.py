from abc import ABC, abstractmethod


class LaunchpadBase(ABC):
    @abstractmethod
    def generate_launchpad(self):
        pass
