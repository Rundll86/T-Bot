from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.event.event_subscriber import EventSubscriber
from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.world.target import BaseWorldTarget
from t_bot.transform.vector import Vector2i


class GameWorld(EventBus):
    def __init__(self) -> None:
        self.input = EventSubscriber()
        self.targets: list[BaseWorldTarget] = []
        super().__init__()

    def add_target(self, target: BaseWorldTarget) -> BaseWorldTarget:
        self.targets.append(target)
        target.join_world.emit(self)
        return target

    def send_input(self, char: str) -> None:
        self.input.emit(char)

    def register_events(self):
        super().register_events()

        @self.input.subscribe
        def input(char: str):
            for target in self.targets:
                target.input.emit(char)


class WorldRenderer(BaseRenderer):
    def __init__(self, world: GameWorld) -> None:
        super().__init__()
        self.size: Vector2i = Vector2i.one() * 20
        self.world = world

    def render(self) -> None:
        self.add_line(f"*{'**' * self.size.x}*")
        for _ in range(self.size.y):
            self.add_line(f"*{'  ' * self.size.x}*")
        self.add_line(f"*{'**' * self.size.x}*")
        for target in self.world.targets:
            self.replace_at(
                (target.position * Vector2i(target.space_count, 1)) + Vector2i.one(),
                target.render(),
                target.space_count,
            )
