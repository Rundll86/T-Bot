import random

from t_bot.content.bullets.slime_sprint import SlimeSprintBullet
from t_bot.content.entities.flower import FlowerEntity
from t_bot.content.entities.player import direction_to_vector
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
            if self.timelifed % 3 == 0:
                match self.is_player_crossed():
                    case True, direction:
                        self.direction = direction
                        for i in range(3):
                            self.world.add_bullet(
                                self,
                                SlimeSprintBullet().set_position(
                                    self.position + direction_to_vector[direction] * i
                                ),
                            )

        @self.subscribe(self.die)
        def die():
            self.world.add_target(FlowerEntity())
