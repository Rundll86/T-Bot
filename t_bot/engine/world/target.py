import copy
from typing import Literal

from rich.color import Color
from rich.style import Style
from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.event.event_subscriber import EventSubscriber
from t_bot.engine.event.logger import GameLogger
from t_bot.engine.game_rule.crit import judge_crit
from t_bot.engine.game_rule.damage import damage_float
from t_bot.engine.renderer.components.progress_bar import ProgressBarRenderer
from t_bot.engine.renderer.effect import BaseEffect
from t_bot.engine.renderer.effects.hurt import HurtEffect
from t_bot.engine.renderer.structs import BaseRenderable
from t_bot.transform.direction import Direction
from t_bot.transform.vector import Vector2i


class BaseWorldTarget(BaseRenderable, EventBus):
    def __init__(self, texture: str) -> None:
        self.join_world = EventSubscriber()
        self.aged = EventSubscriber()
        self.my_turn = EventSubscriber()
        self.die = EventSubscriber()
        super().__init__(2)
        self.position: Vector2i = Vector2i.zero()
        self.texture: str = texture
        self.effects: list["BaseEffect"] = []
        self.background: Color = Color.from_rgb(0, 0, 0)
        self.foreground: Color = Color.from_rgb(255, 255, 255)
        self.direction: Direction = Direction.UP
        self.z_order: int = 0
        self.timelifed: int = 0
        self.speed: float = 1
        self.action_progress: float = 0

    def render(self) -> Text:
        return Text(
            self.texture,
            style=Style(color=self.foreground, bgcolor=self.background)
            + self.blend_output,
        )

    def set_position(self, newpos: Vector2i):
        self.position = newpos
        return self

    def register_events(self):
        super().register_events()

        @self.subscribe(RoundController.time_went)
        def next_round(input: str):
            self.timelifed += 1
            self.aged.emit(self.timelifed)
            self.action_progress += self.speed
            while self.action_progress >= 1:
                self.action_progress -= 1
                self.my_turn.emit()

    def public_die(self):
        self.world.target_died.emit(self)
        self.die.emit()
        # self.unsubscribe_all()

    def move(self, delta: Vector2i):
        old_pos = self.position
        new_pos = Vector2i.from_tuple(self.position + delta).clamp(
            0,
            self.world.size.x - 1,
            0,
            self.world.size.y - 1,
        )
        self.position = new_pos
        return old_pos, new_pos

    @property
    def world(self):
        return GameController.world

    @property
    def blend_output(self) -> Style:
        base = Style()
        for effect in self.effects:
            base += effect.style
        return base


class BaseCollider(BaseWorldTarget):
    def __init__(self, texture: str) -> None:
        self.collided_with = EventSubscriber()
        super().__init__(texture)
        self.hitbox = True
        self.obstructive = False

    def move(self, delta: Vector2i):
        old_pos, new_pos = super().move(delta)
        if new_pos == old_pos or not self.obstructive:
            return old_pos, new_pos
        for target in self.world.targets:
            if target is self:
                continue
            if (
                isinstance(target, BaseCollider)
                and target.hitbox
                and target.obstructive
            ):
                if target.position == new_pos:
                    self.position = old_pos
                    return old_pos, old_pos
        return old_pos, new_pos


class BaseEntity(BaseCollider):
    def __init__(self, display_name: str, max_health: float, texture: str) -> None:
        super().__init__(texture)
        self.z_order = 2
        self.obstructive = True
        self.display_name = display_name
        self.max_health = max_health
        self.current_health = self.max_health
        self.is_player = False
        self.crit_rate = 0.05
        self.crit_damage = 1
        self.anti_crit = 0
        self.health_bar = ProgressBarRenderer(20)

    def register_events(self):
        super().register_events()

        @self.subscribe(self.collided_with)
        def collided_with(collider: BaseCollider):
            if not isinstance(collider, BaseBullet) or collider.launcher is None:
                return
            if collider.launcher.is_player != self.is_player:
                crit, dmg = judge_crit(collider, self)
                self.take_damage(dmg, crit)
                if collider.penetrate_count > 0:
                    collider.penetrate_count -= 1
                if collider.penetrate_count == 0:
                    collider.public_die()

        @self.subscribe(self.die)
        def die():
            from t_bot.engine.controller.wave_controller import WaveController

            WaveController.judge_next()

    def take_damage(self, dmg: float, crit: bool) -> float:
        total_dmg = damage_float(dmg)
        self.current_health -= total_dmg
        if self.is_player:
            GameLogger.add_log(Text(f"受到了{total_dmg}点伤害！", style="#ff0000"))
        else:
            GameController.focus_enemy = self
            if crit:
                GameLogger.add_log(
                    Text(
                        f"造成了{total_dmg}点暴击伤害！",
                        style=Style(color=Color.from_rgb(255, 251, 13)),
                    )
                )
            else:
                GameLogger.add_log(f"造成了{total_dmg}点伤害！")
        self.health_bar.max_value = self.max_health
        self.health_bar.current_value = self.current_health
        HurtEffect().apply(self)
        if self.current_health <= 0:
            self.public_die()
        return total_dmg

    def public_die(self):
        GameLogger.add_log(f"{self.display_name}已被打败！")
        return super().public_die()

    def follow_player(self, speed: int = 1):
        delta = (GameController.player.position - self.position).normalized.round()
        self.move(delta * speed)

    def is_player_crossed(
        self,
    ) -> tuple[Literal[True], Direction] | tuple[Literal[False], None]:
        player = GameController.player
        if player.position.x == self.position.x:
            if player.position.y < self.position.y:
                return True, Direction.UP
            elif player.position.y > self.position.y:
                return True, Direction.DOWN
        elif player.position.y == self.position.y:
            if player.position.x < self.position.x:
                return True, Direction.LEFT
            elif player.position.x > self.position.x:
                return True, Direction.RIGHT
        return False, None


class BaseBullet(BaseCollider):
    def __init__(self, texture: str) -> None:
        super().__init__(texture)
        self.z_order = 1
        self.penetrate_count = 1
        self.lifetime: int = -1
        self.launcher: BaseEntity | None = None
        self.base_damage = 10
        self.crit_rate: float = 0

    def register_events(self):
        super().register_events()

        @self.subscribe(self.aged)
        def aged(timelifed: int):
            if self.lifetime > 0:
                if timelifed > self.lifetime:
                    self.public_die()


class BulletGroup:
    def __init__(self, base_space: list[BaseBullet]) -> None:
        self.base_space = base_space

    def fetch(self, direction: Direction, base_position: Vector2i) -> list[BaseBullet]:
        if direction == Direction.RIGHT:

            def rotate(position: Vector2i):
                return position
        elif direction == Direction.UP:

            def rotate(position: Vector2i):
                return position.rotated_right()
        elif direction == Direction.LEFT:

            def rotate(position: Vector2i):
                return position.rotated_right().rotated_right()
        elif direction == Direction.DOWN:

            def rotate(position: Vector2i):
                return position.rotated_left()

        new_space: list[BaseBullet] = []
        for bullet in self.base_space:
            bullet_cloned = copy.copy(bullet)
            bullet_cloned.join_world = EventSubscriber()
            bullet_cloned.aged = EventSubscriber()
            bullet_cloned.collided_with = EventSubscriber()
            bullet_cloned.register_events()
            bullet_cloned.timelifed = 0
            bullet_cloned.set_position(rotate(bullet.position) + base_position)
            new_space.append(bullet_cloned)
        return new_space
