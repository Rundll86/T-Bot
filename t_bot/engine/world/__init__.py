import sys

from rich.style import Style
from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.event.event_subscriber import EventSubscriber
from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.util.color import blend_colors
from t_bot.engine.world.target import (
    BaseBullet,
    BaseCollider,
    BaseEntity,
    BaseWorldTarget,
)
from t_bot.transform.vector import Vector2i


class GameWorld(EventBus):
    def __init__(self) -> None:
        GameController.world = self
        self.input = EventSubscriber()
        self.target_died = EventSubscriber()
        self.targets: list[BaseWorldTarget] = []
        self.size: Vector2i = Vector2i(20, 20)
        super().__init__()

    def add_target(self, *targets: BaseWorldTarget) -> tuple[BaseWorldTarget, ...]:
        for target in targets:
            if isinstance(target, BaseBullet) and target.launcher is None:
                raise Exception("添加的子弹目标里没有launcher。")
            target.join_world.emit(self)
            self.targets.append(target)
        return targets

    def add_bullet(
        self,
        launcher: BaseEntity,
        *bullets: BaseBullet,
    ) -> tuple[BaseBullet, ...]:
        for bullet in bullets:
            bullet.launcher = launcher
            self.add_target(bullet)
        return bullets

    def register_events(self):
        super().register_events()

        @self.subscribe(self.input)
        def input(char: str):
            if char == "e":
                sys.exit(0)

        @self.subscribe(self.target_died)
        def target_died(target: BaseWorldTarget):
            while target in self.targets:
                self.targets.remove(target)
            del target

    def detect_collision(self):
        for target in self.targets:
            if isinstance(target, BaseCollider) and target.hitbox:
                for next_target in self.targets:
                    if isinstance(next_target, BaseCollider) and next_target.hitbox:
                        if target.position == next_target.position:
                            target.collided_with.emit(next_target)

    @property
    def enemy_count(self) -> int:
        result = 0
        for target in self.targets:
            if isinstance(target, BaseEntity):
                if not target.is_player:
                    result += 1
        return result


class WorldRenderer(BaseRenderer):
    def __init__(self, world: GameWorld) -> None:
        super().__init__()
        self.world = world
        self.size: Vector2i = self.world.size

    def render(self) -> None:
        self.add_line(f"*{'**' * self.size.x}*")
        for y in range(self.size.y):
            self.add_line("*")
            for x in range(self.size.x):
                targets_at_pos = [
                    t for t in self.world.targets if t.position == Vector2i(x, y)
                ]
                if targets_at_pos:
                    targets_at_pos.sort(key=lambda t: t.z_order, reverse=True)
                    top = targets_at_pos[0]
                    blended_bg = blend_colors(*(t.background for t in targets_at_pos))
                    self.append_current(
                        Text(
                            top.texture,
                            style=Style(color=top.foreground, bgcolor=blended_bg)
                            + top.blend_output,
                        )
                    )
                else:
                    self.append_current("  ")
            self.append_current("*")
        self.add_line(f"*{'**' * self.size.x}*")
        pass
