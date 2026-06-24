from abc import abstractmethod

from t_bot.engine.renderer.structs import BaseRenderable


class BaseWorldTarget(BaseRenderable):
    pass


class BaseCollider(BaseWorldTarget):
    @abstractmethod
    def collide_with(self, other: "BaseCollider"):
        pass


class BaseEntity(BaseCollider):
    def __init__(self, display_name: str, max_health: float) -> None:
        super().__init__()
        self.display_name = display_name
        self.max_health = max_health
        self.current_health = self.max_health
