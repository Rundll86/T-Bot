from abc import ABC, abstractmethod

from rich.text import Text

from t_bot.engine.util.character import get_space_count
from t_bot.transform.vector import Vector2i


class BaseRenderer(ABC):
    def __init__(self) -> None:
        self.buffer: list[Text] = []

    @abstractmethod
    def render(self) -> None:
        pass

    def add_line(self, line: str | Text) -> None:
        if isinstance(line, str):
            line = Text.from_markup(line)
        self.buffer.append(line)

    def append_current(self, data: str | Text) -> None:
        if isinstance(data, str):
            data = Text.from_markup(data)
        self.buffer[-1] = self.buffer[-1] + data

    def replace_at(
        self,
        position: Vector2i,
        new_str: str | Text,
        length_override: int = -1,
    ) -> None:
        if isinstance(new_str, str):
            new_str = Text.from_markup(new_str)
        n = length_override if length_override >= 0 else len(new_str.plain)
        row = position.y
        col = position.x
        while len(self.buffer) <= row:
            self.buffer.append(Text(""))
        line = self.buffer[row]
        current_len = len(line.plain)
        if current_len < col:
            line = line + Text(" " * (col - current_len))
        if len(line.plain) < col + n:
            line = line + Text(" " * (col + n - len(line.plain)))
        parts = line.divide([col, col + n])
        line = parts[0] + new_str + parts[2]
        self.buffer[row] = line

    def auto_replace(
        self,
        position: Vector2i,
        new_str: str | Text,
    ):
        self.replace_at(position, new_str, get_space_count(str(new_str)))

    def clear(self) -> None:
        self.buffer.clear()

    def read(self) -> str:
        return "\n".join(line.markup for line in self.buffer)

    def redraw(self) -> str:
        self.clear()
        self.render()
        return self.read()
