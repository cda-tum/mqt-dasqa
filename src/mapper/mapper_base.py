from abc import ABC, abstractmethod


class MapperBase(ABC):
    @abstractmethod
    def map(self):
        pass
