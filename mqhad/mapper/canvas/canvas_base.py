from abc import ABC, abstractmethod


class CanvasBase(ABC):
    @abstractmethod
    def get_canvas(self):
        pass

    @abstractmethod
    def update_components(self, component_name, option_name, option_value):
        pass
