from rich.color import Color

from t_bot.engine.world.target import BaseBullet


class PlayerSword(BaseBullet):
    def __init__(self) -> None:
        super().__init__("剑")
        self.style.from_color(Color.from_rgb(255, 0, 0))
