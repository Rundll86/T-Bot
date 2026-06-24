from rich.style import Style
from rich.text import Text

from t_bot.engine.event.event_subscriber import EventSubscriber
from t_bot.engine.renderer.structs import BaseRenderable
from t_bot.transform.vector import Vector2i


class BaseWorldTarget(BaseRenderable):
    def __init__(self, texture: str) -> None:
        super().__init__(2)
        self.position: Vector2i = Vector2i.zero()
        self.texture: str = texture
        self.style = Style(color="white", bgcolor="black")
        self.background: str = "black"
        self.foreground: str = "white"
        self.listen_events()
        self.register_events()

    def listen_events(self):
        self.join_world = EventSubscriber()

    def register_events(self):
        pass

    def render(self) -> Text:
        return Text(self.texture, style=self.style)


class BaseCollider(BaseWorldTarget):
    def listen_events(self):
        super().listen_events()
        self.collided_with = EventSubscriber()


class BaseEntity(BaseCollider):
    def __init__(self, display_name: str, max_health: float, texture: str) -> None:
        super().__init__(texture)
        self.display_name = display_name
        self.max_health = max_health
        self.current_health = self.max_health


class BaseBullet(BaseCollider):
    pass
