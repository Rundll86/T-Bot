from abc import ABC, abstractmethod

from t_bot.transform.vector import Vector2i


class BaseRenderer(ABC):
    def __init__(self) -> None:
        self.buffer: list[str] = []

    @abstractmethod
    def render(self) -> None:
        pass

    def add_line(self, line: str) -> None:
        self.buffer.append(line)

    def replace_at(
        self,
        position: Vector2i,
        new_str: str,
        length_override: int = -1,
    ) -> None:
        n = length_override if length_override >= 0 else len(new_str)
        row = position.y
        col = position.x
        while len(self.buffer) <= row:
            self.buffer.append("")
        line = self.buffer[row]
        if len(line) < col:
            line = line.ljust(col)
        line = line[:col] + new_str + line[col + n :]
        self.buffer[row] = line

    def read(self) -> str:
        return "\n".join(self.buffer)

    def refresh(self) -> str:
        self.render()
        return self.read()
