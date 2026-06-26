from rich.color import Color

from t_bot.engine.world.target import BaseBullet


class PlayerSwordLight(BaseBullet):
    def __init__(self) -> None:
        super().__init__(-1, "光")
        self.foreground = Color.from_rgb(0, 0, 0)
        self.background = Color.from_rgb(255, 255, 255)
        self.lifetime = 1
