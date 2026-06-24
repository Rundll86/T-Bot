from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    def __init__(self) -> None:
        self.buffer: list[str] = []

    @abstractmethod
    def render(self) -> None:
        pass

    def add_line(self, line: str) -> None:
        self.buffer.append(line)

    def read(self) -> str:
        return "\n".join(self.buffer)
