from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.event.logger import GameLogger
from t_bot.engine.world.target import BaseEntity


class GrassEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("杂草", 1, "草")

    def register_events(self):
        super().register_events()

        @self.subscribe(self.die)
        def die():
            GameController.player.attack_force += 3
            GameLogger.add_log(Text("攻击力+3", style="#00ff00"))
