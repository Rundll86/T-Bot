from t_bot.engine.event.logger import GameLogger
from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.renderer.components.progress_bar import ProgressBarRenderer
from t_bot.transform.vector import Vector2i


class PlayerUIRenderer(BaseRenderer):
    def __init__(self, size: int) -> None:
        super().__init__()
        self.size = size
        self.health_bar = ProgressBarRenderer(20)

    def render(self) -> None:
        self.add_line("-" * (self.size + 2))
        for _ in range(4):
            self.add_line(f"|{' ' * self.size}|")
        self.add_line("-" * (self.size + 2))
        self.add_line("|")
        self.add_line("-" * (self.size + 2))
        self.replace_at(Vector2i(3, 2), "生命值", 6)
        self.replace_at(Vector2i(3, 3), " - " + self.health_bar.redraw())
        self.replace_at(Vector2i(3, 6), str(GameLogger.latest()))
