from typing import TYPE_CHECKING

from rich.style import Style


from t_bot.content.bullets.player_sword import PlayerSword
from t_bot.content.bullets.player_sword_light import PlayerSwordLight
from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.world.target import BaseEntity, BulletGroup
from t_bot.transform.vector import Vector2i
from t_bot.transform.direction import direction_to_vector, input_to_direction

if TYPE_CHECKING:
    pass


class PlayerEntity(BaseEntity):
    def __init__(self) -> None:
        GameController.player = self
        super().__init__("我", 100, "我")
        self.is_player = True
        self.style += Style(bold=True)
        self.sword = PlayerSword()
        self.attack_counter = 0
        self.sword_group0 = BulletGroup([PlayerSword().set_position(Vector2i(0, 1))])
        self.sword_group1 = BulletGroup([PlayerSword().set_position(Vector2i(0, -1))])
        self.sword_group2 = BulletGroup([PlayerSword().set_position(Vector2i(3, 0))])
        self.sword_group3 = BulletGroup([PlayerSword().set_position(Vector2i(1, 0))])
        self.attack1 = BulletGroup(
            [
                PlayerSwordLight().set_position(Vector2i(1, 1)),
                PlayerSwordLight().set_position(Vector2i(1, 0)),
                PlayerSwordLight().set_position(Vector2i(1, -1)),
            ]
        )
        self.attack2 = BulletGroup(
            [
                PlayerSwordLight().set_position(Vector2i(1, 0)),
                PlayerSwordLight().set_position(Vector2i(2, 0)),
            ]
        )

    def register_events(self):
        @self.subscribe(self.world.input)
        def input(char: str):
            if char in input_to_direction:
                direction = input_to_direction[char]
                delta = direction_to_vector[direction]
                self.move(delta)
                self.direction = direction
                self.update_sword(self.sword_group0)
                self.attack_counter = 0
            else:
                match char:
                    case "j":
                        delta = Vector2i.from_tuple(self.sword.position - self.position)
                        match self.attack_counter % 5:
                            case 0:
                                self.update_sword(self.sword_group1)
                                self.world.add_bullet(
                                    self,
                                    *self.attack1.fetch(
                                        self.direction,
                                        self.position,
                                    ),
                                )
                            case 1:
                                self.update_sword(self.sword_group0)
                                self.world.add_bullet(
                                    self,
                                    *self.attack1.fetch(
                                        self.direction,
                                        self.position,
                                    ),
                                )
                            case 2:
                                self.update_sword(self.sword_group2)
                                self.world.add_bullet(
                                    self,
                                    *self.attack2.fetch(
                                        self.direction,
                                        self.position,
                                    ),
                                )
                            case 3:
                                self.update_sword(self.sword_group3)
                            case 4:
                                self.update_sword(self.sword_group0)
                        self.attack_counter += 1
                        self.sword.hitbox = True

    def update_sword(self, group: BulletGroup):
        self.sword.public_die()
        self.sword = group.fetch(self.direction, self.position)[0]
        self.sword.hitbox = False
        self.world.add_bullet(self, self.sword)
