from abc import ABC, abstractmethod


class BaseRenderable(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
