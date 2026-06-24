from rich.color import Color
from rich.style import Style

from t_bot.engine.world.target import BaseBullet


class PlayerSword(BaseBullet):
    def __init__(self) -> None:
        super().__init__("剑")
        self.style += Style(color=Color.from_rgb(10, 10, 10))
