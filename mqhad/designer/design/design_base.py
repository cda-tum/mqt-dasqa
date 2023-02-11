from abc import ABC, abstractmethod


class DesignBase(ABC):
    @abstractmethod
    def get_design(self):
        pass
