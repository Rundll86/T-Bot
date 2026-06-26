from rich.color import Color
from rich.style import Style
from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.event.logger import GameLogger
from t_bot.engine.renderer import BaseRenderer
from t_bot.transform.vector import Vector2i


class PlayerUIRenderer(BaseRenderer):
    def __init__(self, size: int) -> None:
        super().__init__()
        self.size = size

    def render(self) -> None:
        self.add_line("-" * (self.size + 2))
        for _ in range(4):
            self.add_line(f"|{' ' * self.size}|")
        self.add_line("-" * (self.size + 2))
        for _ in range(4):
            self.add_line(f"|{' ' * self.size}|")
        self.add_line("-" * (self.size + 2))
        self.add_line("|")
        self.add_line("-" * (self.size + 2))
        # 玩家状态
        self.replace_at(Vector2i(3, 2), "生命值", 6)
        self.replace_at(
            Vector2i(3, 3),
            " - " + GameController.player.health_bar.redraw(),
        )
        # 日志
        self.replace_at(
            Vector2i(3, 11),
            GameLogger.latest()
            if GameLogger.have_log()
            else Text("行动日志...", style=Style(color=Color.from_rgb(100, 100, 100))),
        )
        # 敌人状态
        self.replace_at(Vector2i(3, 7), "敌人状态", 8)
        if GameController.focus_enemy is not None:
            self.replace_at(
                Vector2i(3, 8),
                " - " + GameController.focus_enemy.health_bar.redraw(),
            )
        else:
            self.replace_at(
                Vector2i(3, 8),
                Text("未进入战斗", style=Style(color=Color.from_rgb(100, 100, 100))),
                10,
            )
