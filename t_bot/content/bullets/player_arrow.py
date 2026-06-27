from rich.color import Color

from t_bot.engine.world.target import BaseBullet
from t_bot.transform.direction import direction_to_vector


class PlayerArrow(BaseBullet):
    def __init__(self) -> None:
        super().__init__("箭")
        self.foreground = Color.from_rgb(255, 255, 200)
        self.speed = 1
        self.lifetime = 10
        self.penetrate_count = 3
        self.base_damage = 15

    def register_events(self):
        super().register_events()

        @self.subscribe(self.my_turn)
        def my_turn():
            delta = direction_to_vector[self.direction]
            old_pos, new_pos = self.move(delta)
            if old_pos == new_pos:
                self.public_die()
