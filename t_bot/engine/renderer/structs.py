from abc import ABC, abstractmethod

from rich.text import Text


class BaseRenderable(ABC):
    def __init__(self, space_count: int = 1) -> None:
        super().__init__()
        self.space_count = space_count

    @abstractmethod
    def render(self) -> str | Text:
        pass
