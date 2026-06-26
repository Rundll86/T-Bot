import random

from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.event.logger import GameLogger
from t_bot.engine.world.target import BaseEntity


class FlowerEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("花朵", 1, "花")

    def register_events(self):
        super().register_events()

        @self.subscribe(self.die)
        def die():
            GameController.player.max_health += 5
            GameController.player.current_health += 5
            GameLogger.add_log(Text("生命上限+5", style="#00ff00"))


class GrassEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("杂草", 1, "草")

    def register_events(self):
        super().register_events()

        @self.subscribe(self.die)
        def die():
            GameController.player.attack_force += 3
            GameLogger.add_log(Text("攻击力+3", style="#00ff00"))


class DurainEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("榴莲", 30, "榴")

    def register_events(self):
        super().register_events()

        @self.subscribe(self.die)
        def die():
            if random.random() < 0.4:
                GameController.player.crit_rate += 0.02
                GameLogger.add_log(Text("暴击率+2%", style="#00ff00"))
            else:
                GameController.player.crit_damage += 0.06
                GameLogger.add_log(Text("暴击伤害+6%", style="#00ff00"))


class FishEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("三文鱼", 1, "鱼")

    def register_events(self):
        super().register_events()

        @self.subscribe(self.die)
        def die():
            value = random.uniform(0.01, 0.06)
            GameController.player.speed += value
            GameLogger.add_log(Text(f"速度+{value:.2f}", style="#00ff00"))


powerups = [FlowerEntity, GrassEntity, DurainEntity, FishEntity]
