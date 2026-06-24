from t_bot.content.entities.player import PlayerEntity
from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.world.target import BaseWorldTarget
from t_bot.transform.vector import Vector2i


class GameWorld:
    def __init__(self) -> None:
        self.targets: list[BaseWorldTarget] = []

    def init(self):
        self.add_target(PlayerEntity())

    def add_target(self, target: BaseWorldTarget) -> BaseWorldTarget:
        self.targets.append(target)
        target.join_world.emit(self)
        return target


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
                target.position + Vector2i.one(),
                target.render(),
                target.space_count,
            )
