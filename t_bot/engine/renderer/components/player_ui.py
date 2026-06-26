from rich.color import Color
from rich.style import Style
from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.event.logger import GameLogger
from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.util.character import get_space_count
from t_bot.transform.vector import Vector2i


class PlayerUIRenderer(BaseRenderer):
    def __init__(self, size: int) -> None:
        super().__init__()
        self.size = size
        self.show_log_count = 3

    def render(self) -> None:
        # 玩家UI
        self.add_line("-" * (self.size + 2))
        for _ in range(8):
            self.add_line(f"|{' ' * self.size}|")
        self.add_line("-" * (self.size + 2))
        # 敌人UI
        for _ in range(4):
            self.add_line(f"|{' ' * self.size}|")
        self.add_line("-" * (self.size + 2))
        # 行动日志
        for _ in range(self.show_log_count):
            self.add_line("|")
        self.add_line("-" * (self.size + 2))
        # 玩家状态
        self.auto_replace(
            Vector2i(3, 2),
            f"生命值 <{GameController.player.current_health}/{GameController.player.max_health}>",
        )
        self.replace_at(
            Vector2i(3, 3),
            GameController.player.health_bar.redraw(),
        )
        self.auto_replace(
            Vector2i(3, 5), f"攻击力 {GameController.player.attack_force}"
        )
        # 敌人状态
        if (
            GameController.focus_enemy is not None
            and GameController.focus_enemy in GameController.world.targets
        ):
            self.replace_at(
                Vector2i(3, 11),
                GameController.focus_enemy.display_name,
                get_space_count(GameController.focus_enemy.display_name),
            )
            self.replace_at(
                Vector2i(5, 12),
                GameController.focus_enemy.health_bar.redraw()
                + f" {GameController.focus_enemy.current_health:.0f}/{GameController.focus_enemy.max_health:.0f}",
            )
        else:
            self.replace_at(Vector2i(3, 11), "敌人状态", 8)
            self.replace_at(
                Vector2i(5, 12),
                Text("未进入战斗", style=Style(color=Color.from_rgb(100, 100, 100))),
                10,
            )
        # 日志
        i = 0
        for log in GameLogger.read(self.show_log_count):
            self.replace_at(Vector2i(3, 15 + i), log)
            i += 1
