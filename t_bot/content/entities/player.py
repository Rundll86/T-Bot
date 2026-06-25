from typing import TYPE_CHECKING

from rich.style import Style

from t_bot.content.bullets.player_sword import PlayerSword
from t_bot.content.bullets.player_sword_light import PlayerSwordLight
from t_bot.engine.world.target import BaseEntity, BulletGroup
from t_bot.transform.vector import Vector2i
from t_bot.transform.direction import direction_to_vector, input_to_direction

if TYPE_CHECKING:
    from t_bot.engine.world import GameWorld


class PlayerEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("我", 100, "我")
        self.sword = PlayerSword()
        self.sword.position += Vector2i(1, 0)
        self.style = self.style + Style()
        self.attack_counter = 0
        self.attack1 = BulletGroup(
            [
                PlayerSwordLight().set_position(Vector2i(1, 1)),
                PlayerSwordLight().set_position(Vector2i(1, 0)),
                PlayerSwordLight().set_position(Vector2i(1, -1)),
                PlayerSwordLight().set_position(Vector2i(0, -1)),
            ]
        )

    def register_events(self):
        @self.subscribe(self.join_world)
        def join_world(world: "GameWorld"):
            world.add_target(self.sword)

        @self.subscribe(self.world.input)
        def input(char: str):
            if char in input_to_direction:
                direction = input_to_direction[char]
                delta = direction_to_vector[direction]
                self.position += delta
                self.direction = direction
                self.sword.position = self.position + delta.rotated_left()
            else:
                match char:
                    case "j":
                        delta = self.sword.position - self.position
                        match self.attack_counter % 3:
                            case 0:
                                self.world.add_target(
                                    *self.attack1.fetch(
                                        self.direction,
                                        self.position,
                                    )
                                )
