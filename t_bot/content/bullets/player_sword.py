from rich.color import Color

from t_bot.engine.world.target import BaseBullet


class PlayerSword(BaseBullet):
    def __init__(self) -> None:
        super().__init__("剑")
        self.foreground = Color.from_rgb(200, 200, 200)
        self.penetrate_count = -1
