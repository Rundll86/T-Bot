import math

from rich.color import Color
from rich.style import Style
from rich.text import Text

from t_bot.engine.renderer import BaseRenderer
from t_bot.transform.vector import Vector2i


class ProgressBarRenderer(BaseRenderer):
    def __init__(
        self,
        length: int,
        max_value: float = 100,
        front_char: str = "#",
        back_char: str = "-",
        decorated: bool = True,
        front_color: str | Color = Color.from_rgb(0, 255, 0),
        back_color: str | Color = "red",
    ) -> None:
        super().__init__()
        self.max_value = max_value
        self.current_value = max_value
        self.length = length
        self.front_char = front_char
        self.back_char = back_char
        self.decorated = decorated
        self.front_color = front_color
        self.back_color = back_color

    def get_progress(self) -> float:
        return self.current_value / self.max_value

    def get_frontend(self) -> int:
        return max(math.ceil(self.length * self.get_progress()), 0)

    def render(self) -> None:
        self.add_line("")
        prefix = Text("\\[ ") if self.decorated else Text("")
        suffix = Text(" ]") if self.decorated else Text("")
        self.replace_at(
            Vector2i(0, 0),
            prefix
            + Text(
                self.front_char * self.get_frontend(),
                style=Style(color=self.front_color),
            )
            + Text(
                self.back_char * (self.length - self.get_frontend()),
                style=Style(color=self.back_color),
            )
            + suffix,
        )
