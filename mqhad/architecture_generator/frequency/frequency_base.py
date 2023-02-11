from abc import ABC, abstractmethod


class FrequencyBase(ABC):
    @abstractmethod
    def get_frequency_allocation(self):
        pass
