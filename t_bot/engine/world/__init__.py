from t_bot.engine.renderer import BaseRenderer
from t_bot.transform.vector import Vector2i


class WorldRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.size: Vector2i = Vector2i.one() * 20

    def render(self) -> None:
        self.add_line(f"*{'**' * self.size.x}*")
        for _ in range(self.size.y):
            self.add_line(f"*{'  ' * self.size.x}*")
        self.add_line(f"*{'**' * self.size.x}*")


class GameWorld:
    pass
