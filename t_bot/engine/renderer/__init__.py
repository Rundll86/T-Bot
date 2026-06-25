from abc import ABC, abstractmethod

from rich.text import Text

from t_bot.transform.vector import Vector2i


class BaseRenderer(ABC):
    def __init__(self) -> None:
        self.buffer: list[str] = []

    @abstractmethod
    def render(self) -> None:
        pass

    def add_line(self, line: str) -> None:
        self.buffer.append(line)

    def append_current(self, data: str) -> None:
        self.buffer[-1] += data

    def clear(self) -> None:
        self.buffer.clear()

    def replace_at(
        self,
        position: Vector2i,
        new_str: str | Text,
        length_override: int = -1,
    ) -> None:
        if isinstance(new_str, Text):
            middle = new_str
            visible_len = len(new_str.plain)
        else:
            middle = Text(new_str)
            visible_len = len(new_str)

        n = length_override if length_override >= 0 else visible_len
        row = position.y
        col = position.x

        while len(self.buffer) <= row:
            self.buffer.append("")

        line = self.buffer[row]
        line_text = Text.from_markup(line) if line else Text("")

        current_len = len(line_text.plain)
        if current_len < col:
            line_text = line_text + Text(" " * (col - current_len))
        if len(line_text.plain) < col + n:
            line_text = line_text + Text(" " * (col + n - len(line_text.plain)))

        parts = line_text.divide([col, col + n])
        result = parts[0] + middle + parts[2]
        self.buffer[row] = result.markup

    def read(self) -> str:
        return "\n".join(self.buffer)

    def redraw(self) -> str:
        self.clear()
        self.render()
        return self.read()
