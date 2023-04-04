from abc import ABC, abstractmethod


class DesignBase(ABC):
    @abstractmethod
    def design(self):
        pass
