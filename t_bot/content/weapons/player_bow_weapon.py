from t_bot.content.bullets.player_arrow import PlayerArrow
from t_bot.engine.world.target import BaseWeapon
from t_bot.transform.direction import direction_to_vector
from t_bot.transform.vector import Vector2i


class PlayerBowWeapon(BaseWeapon):
    def __init__(self) -> None:
        super().__init__("弓")
        self.charging: int = 0
        self.visual_groups: list[list[Vector2i]] = [
            [Vector2i(1, 0)],
        ]

    def get_position(self, index: int) -> Vector2i:
        assert self.player is not None
        direction = self.player.direction
        rel = self.visual_groups[index][0]
        return rel.rotated_by_direction(direction) + self.player.position

    def player_moved(self) -> None:
        assert self.player is not None
        self.position = self.get_position(0)

    def attack(self) -> None:
        assert self.player is not None
        player = self.player
        self.charging += 1
        if self.charging >= 3:
            self.charging = 0
            direction = player.direction
            arrow = PlayerArrow()
            arrow.direction = direction
            arrow.set_position(player.position + direction_to_vector[direction])
            player.world.add_bullet(player, arrow)
