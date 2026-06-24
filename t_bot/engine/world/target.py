from abc import abstractmethod

from t_bot.engine.renderer.structs import BaseRenderable
from t_bot.transform.vector import Vector2i


class BaseWorldTarget(BaseRenderable):
    def __init__(self, texture: str) -> None:
        super().__init__(2)
        self.position: Vector2i = Vector2i.zero()
        self.texture: str = texture
        self.background: str = "black"
        self.foreground: str = "white"

    def render(self) -> str:
        return f"[{self.foreground} on {self.background}]{self.texture}[/{self.foreground} on {self.background}]"


class BaseCollider(BaseWorldTarget):
    @abstractmethod
    def collide_with(self, other: "BaseCollider"):
        pass


class BaseEntity(BaseCollider):
    def __init__(self, display_name: str, max_health: float, texture: str) -> None:
        super().__init__(texture)
        self.display_name = display_name
        self.max_health = max_health
        self.current_health = self.max_health
