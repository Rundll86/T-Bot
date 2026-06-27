from t_bot.content.bullets.player_sword_light import PlayerSwordLight
from t_bot.engine.controller.audio_controller import AudioController
from t_bot.engine.world.target import BaseWeapon, BulletGroup
from t_bot.transform.vector import Vector2i


class PlayerSwordWeapon(BaseWeapon):
    def __init__(self) -> None:
        super().__init__("重剑", "剑")
        self.attack_counter: int = 0
        self.visual_groups: list[list[Vector2i]] = [
            [Vector2i(0, 1)],
            [Vector2i(0, -1)],
            [Vector2i(3, 0)],
            [Vector2i(1, 0)],
        ]
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

    def get_position(self, index: int) -> Vector2i:
        assert self.player is not None
        direction = self.player.direction
        rel = self.visual_groups[index][0]
        return rel.rotated_by_direction(direction) + self.player.position

    def player_moved(self) -> None:
        assert self.player is not None
        self.attack_counter = 0
        self.position = self.get_position(0)

    def attack(self) -> None:
        assert self.player is not None
        player = self.player
        direction = player.direction
        match self.attack_counter % 5:
            case 0:
                self.position = self.get_position(1)
                player.world.add_bullet(
                    player,
                    *self.attack1.modify(
                        lambda b: b.set_base_damage(player.attack_force * 1.1)
                    ).fetch(direction, player.position),
                )
                AudioController.play("swing1.mp3")
            case 1:
                self.position = self.get_position(0)
                player.world.add_bullet(
                    player,
                    *self.attack1.modify(
                        lambda b: b.set_base_damage(player.attack_force * 0.9)
                    ).fetch(direction, player.position),
                )
                AudioController.play("swing2.mp3")
            case 2:
                self.position = self.get_position(2)
                player.world.add_bullet(
                    player,
                    *self.attack2.modify(
                        lambda b: b.set_base_damage(player.attack_force * 1.5)
                    ).fetch(direction, player.position),
                )
                AudioController.play("swing3.mp3")
            case 3:
                self.position = self.get_position(3)
            case 4:
                self.position = self.get_position(0)
        self.attack_counter += 1
