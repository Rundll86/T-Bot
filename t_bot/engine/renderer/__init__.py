from abc import ABC, abstractmethod

from t_bot.engine.renderer.structs import BaseRenderable


class BaseRenderer(ABC):
    def __init__(self) -> None:
        self.targets: list[BaseRenderable] = []

    @abstractmethod
    def render(self) -> str:
        pass
