import sys

from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.event.event_subscriber import EventSubscriber
from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.world.target import BaseCollider, BaseWorldTarget
from t_bot.transform.vector import Vector2i


class GameWorld(EventBus):
    def __init__(self) -> None:
        self.input = EventSubscriber()
        self.target_died = EventSubscriber()
        super().__init__()
        self.targets: list[BaseWorldTarget] = []

    def add_target(self, *targets: BaseWorldTarget) -> tuple[BaseWorldTarget, ...]:
        self.targets.extend(targets)
        for target in targets:
            target.world = self
            target.join_world.emit(self)
        return targets

    def register_events(self):
        super().register_events()

        @self.input.subscribe
        def input(char: str):
            if char == "e":
                sys.exit(0)
            else:
                for target in self.targets:
                    target.input.emit(char)
                    if isinstance(target, BaseCollider):
                        for next_target in self.targets:
                            if isinstance(next_target, BaseCollider):
                                if target.position == next_target.position:
                                    target.collided_with.emit(next_target)

        @self.target_died.subscribe
        def target_died(target: BaseWorldTarget):
            while target in self.targets:
                print(target)
                self.targets.remove(target)


class WorldRenderer(BaseRenderer):
    def __init__(self, world: GameWorld) -> None:
        super().__init__()
        self.size: Vector2i = Vector2i.one() * 20
        self.world = world

    def render(self) -> None:
        self.add_line(f"*{'**' * self.size.x}*")
        for y in range(self.size.y):
            self.add_line("*")
            for x in range(self.size.y):
                target: BaseWorldTarget | None = None
                for t in self.world.targets:
                    if t.position == Vector2i(x, y):
                        target = t
                if target is not None:
                    self.append_current(target.texture)
                else:
                    self.append_current("  ")
            self.append_current("*")
        self.add_line(f"*{'**' * self.size.x}*")
        pass
