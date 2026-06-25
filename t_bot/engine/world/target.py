import copy

from rich.style import Style
from rich.text import Text

from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.event.event_subscriber import EventSubscriber
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
        self.style = Style(color="white", bgcolor="black")
        self.background: str = "black"
        self.foreground: str = "white"
        self.direction: Direction = Direction.UP
        self.timelifed: int = 0

    def render(self) -> Text:
        return Text(self.texture, style=self.style)

    def set_position(self, newpos: Vector2i):
        self.position = newpos
        return self

    def register_events(self):
        super().register_events()

        @self.world.input.subscribe
        def input(char: str):
            self.timelifed += 1
            self.aged.emit(self.timelifed)

    @property
    def world(self):
        return GameController.world


class BaseCollider(BaseWorldTarget):
    def __init__(self, texture: str) -> None:
        self.collided_with = EventSubscriber()
        super().__init__(texture)


class BaseEntity(BaseCollider):
    def __init__(self, display_name: str, max_health: float, texture: str) -> None:
        super().__init__(texture)
        self.display_name = display_name
        self.max_health = max_health
        self.current_health = self.max_health


class BaseBullet(BaseCollider):
    def __init__(self, penetrate_count: int, texture: str) -> None:
        super().__init__(texture)
        self.penetrate_count = penetrate_count
        self.lifetime: int = -1

    def register_events(self):
        super().register_events()

        @self.collided_with.subscribe
        def collided_with(other: BaseCollider):
            pass

        @self.aged.subscribe
        def aged(timelifed: int):
            if self.lifetime > 0:
                if timelifed >= self.lifetime:
                    self.world.target_died.emit(self)


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
