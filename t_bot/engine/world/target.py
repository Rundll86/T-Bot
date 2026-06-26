import copy

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
from t_bot.engine.renderer.structs import BaseRenderable
from t_bot.transform.direction import Direction
from t_bot.transform.vector import Vector2i


class BaseWorldTarget(BaseRenderable, EventBus):
    def __init__(self, texture: str) -> None:
        self.join_world = EventSubscriber()
        self.aged = EventSubscriber()
        super().__init__(2)
        self.position: Vector2i = Vector2i.zero()
        self.texture: str = texture
        self.style = Style()
        self.background: Color = Color.from_rgb(0, 0, 0)
        self.foreground: Color = Color.from_rgb(255, 255, 255)
        self.direction: Direction = Direction.UP
        self.timelifed: int = 0

    def render(self) -> Text:
        return Text(
            self.texture,
            style=Style(color=self.foreground, bgcolor=self.background) + self.style,
        )

    def set_position(self, newpos: Vector2i):
        self.position = newpos
        return self

    def register_events(self):
        super().register_events()

        @self.subscribe(RoundController.next_round)
        def next_round():
            self.timelifed += 1
            self.aged.emit(self.timelifed)

    def public_die(self):
        self.world.target_died.emit(self)

    @property
    def world(self):
        return GameController.world


class BaseCollider(BaseWorldTarget):
    def __init__(self, texture: str) -> None:
        self.collided_with = EventSubscriber()
        super().__init__(texture)
        self.hitbox = True


class BaseEntity(BaseCollider):
    def __init__(self, display_name: str, max_health: float, texture: str) -> None:
        super().__init__(texture)
        self.display_name = display_name
        self.max_health = max_health
        self.current_health = self.max_health
        self.is_player = False
        self.crit_rate = 0.9
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

    def take_damage(self, dmg: float, crit: bool) -> float:
        total_dmg = damage_float(dmg)
        self.current_health -= total_dmg
        if not self.is_player:
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
        if self.current_health <= 0:
            self.public_die()
        return total_dmg

    def public_die(self):
        GameLogger.add_log(f"{self.display_name}已被打败！")
        return super().public_die()


class BaseBullet(BaseCollider):
    def __init__(self, texture: str) -> None:
        super().__init__(texture)
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
            bullet_cloned.position = rotate(bullet.position) + base_position
            new_space.append(bullet_cloned)
        return new_space
