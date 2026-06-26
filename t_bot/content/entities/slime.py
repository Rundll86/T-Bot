import random

from t_bot.engine.world.target import BaseEntity


class SlimeEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("史莱姆", 100, "史")
        self.speed = random.uniform(0.1, 0.6)

    def register_events(self):
        super().register_events()

        @self.subscribe(self.my_turn)
        def my_turn():
            self.follow_player()
