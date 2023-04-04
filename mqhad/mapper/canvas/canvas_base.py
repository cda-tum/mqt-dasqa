from abc import ABC, abstractmethod


class CanvasBase(ABC):
    @abstractmethod
    def get_canvas(self):
        pass
