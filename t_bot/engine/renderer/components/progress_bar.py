import math

from t_bot.engine.renderer import BaseRenderer


class ProgressBarRenderer(BaseRenderer):
    def __init__(self, length: int, max_value: float = 100) -> None:
        super().__init__()
        self.max_value = max_value
        self.current_value = max_value
        self.length = length

    def get_progress(self) -> float:
        return self.current_value / self.max_value

    def get_frontend(self) -> int:
        return math.ceil(self.length * self.get_progress())

    def render(self) -> None:
        self.add_line(
            f"[ {'#' * self.get_frontend()}{'·' * (self.length - self.get_frontend())} ]"
        )
