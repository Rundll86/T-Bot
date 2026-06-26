import math

from rich.color import Color
from rich.style import Style
from rich.text import Text

from t_bot.engine.renderer import BaseRenderer
from t_bot.transform.vector import Vector2i


class ProgressBarRenderer(BaseRenderer):
    def __init__(self, length: int, max_value: float = 100) -> None:
        super().__init__()
        self.max_value = max_value
        self.current_value = max_value
        self.length = length

    def get_progress(self) -> float:
        return self.current_value / self.max_value

    def get_frontend(self) -> int:
        return max(math.ceil(self.length * self.get_progress()), 0)

    def render(self) -> None:
        self.add_line("")
        self.replace_at(
            Vector2i(0, 0),
            Text("\\[ ")
            + Text(
                "#" * self.get_frontend(), style=Style(color=Color.from_rgb(0, 255, 0))
            )
            + Text("-" * (self.length - self.get_frontend()), style="red")
            + Text(" ]"),
        )
