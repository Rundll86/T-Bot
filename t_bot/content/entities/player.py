from typing import TYPE_CHECKING

from rich.style import Style

from t_bot.content.bullets.player_sword import PlayerSword
from t_bot.engine.world.target import BaseEntity
from t_bot.transform.vector import Vector2i

if TYPE_CHECKING:
    from t_bot.engine.world import GameWorld


class PlayerEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("我", 100, "我")
        self.sword = PlayerSword()
        self.sword.position += Vector2i(1, 0)
        self.style = self.style + Style()

    def register_events(self):
        super().register_events()

        @self.join_world.subscribe
        def join_world(world: "GameWorld"):
            world.add_target(self.sword)
