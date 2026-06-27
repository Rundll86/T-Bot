from typing import TYPE_CHECKING
from rich.style import Style
from t_bot.content.weapons.player_bow_weapon import PlayerBowWeapon
from t_bot.content.weapons.player_sword_weapon import PlayerSwordWeapon
from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.renderer.effects.style_blend import StyleBlendEffect
from t_bot.engine.world import GameWorld
from t_bot.engine.world.target import BaseEntity, BaseWeapon
from t_bot.transform.vector import Vector2i
from t_bot.transform.direction import direction_to_vector, input_to_direction

if TYPE_CHECKING:
    pass


class PlayerEntity(BaseEntity):
    def __init__(self) -> None:
        GameController.player = self
        super().__init__("我", 100, "我")
        self.z_order = 3
        self.is_player = True
        self.effects.append(StyleBlendEffect(Style(bold=True)))
        self.weapons: list[BaseWeapon] = [
            PlayerSwordWeapon().set_player(self),
            PlayerBowWeapon().set_player(self),
        ]
        self.using_weapon: int = 1
        self.attack_force = 10

    def register_events(self):
        super().register_events()

        @self.subscribe(self.join_world)
        def join_world(world: GameWorld):
            for w in self.weapons:
                w.position = self.position + Vector2i(0, 1)
                world.add_target(w)

        @self.subscribe(self.my_turn)
        def my_turn():
            char = RoundController.last_input
            if char in input_to_direction:
                direction = input_to_direction[char]
                delta = direction_to_vector[direction]
                self.move(delta)
                self.direction = direction
                self.weapons[self.using_weapon].player_moved()
            else:
                match char:
                    case "j":
                        self.weapons[self.using_weapon].attack()
                    case "x":
                        self.using_weapon = (self.using_weapon + 1) % len(self.weapons)
                    case "z":
                        self.using_weapon = (self.using_weapon - 1) % len(self.weapons)
