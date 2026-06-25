from rich.color import Color
from rich.style import Style

from t_bot.engine.world.target import BaseBullet


class PlayerSwordLight(BaseBullet):
    def __init__(self) -> None:
        super().__init__(-1, "光")
        self.style += Style(
            color=Color.from_rgb(0, 0, 0), bgcolor=Color.from_rgb(255, 255, 255)
        )
        self.lifetime = 1
